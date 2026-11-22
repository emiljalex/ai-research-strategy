from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import CANONICAL, audit, build
from content import markdown


class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "repository"
        self.root.mkdir()
        for name in ("assets", "content"):
            shutil.copytree(ROOT / name, self.root / name)
        self.drafts = self.base / "drafts"
        section = self.drafts / "methods"
        section.mkdir(parents=True)
        self.draft = section / "a-private-review-example.md"
        self.draft.write_text("---\ntitle: Private review fixture\ndescription: Exercises the review boundary.\nkind: Method\nstatus: draft\norder: 100\n---\nAn unpublished sentence.\n")

    def test_public_and_review_are_separate(self):
        public, _ = build(self.root)
        review, _ = build(self.root, self.drafts)
        self.assertFalse((public / "methods" / self.draft.stem).exists())
        self.assertNotIn("Private review fixture", (public / "index.html").read_text())
        self.assertIn("Founder review draft", (review / "methods" / self.draft.stem / "index.html").read_text())
        self.assertIn('href="methods/a-private-review-example/index.html"', (review / "index.html").read_text())
        self.assertIn("noindex", (public / "_headers").read_text())

    def test_approval_and_rebuild(self):
        public, _ = build(self.root)
        new = self.root / "content" / "methods" / self.draft.name
        new.write_text(self.draft.read_text().replace("status: draft", "status: published"))
        build(self.root)
        self.assertTrue((public / "methods" / self.draft.stem / "index.html").is_file())
        new.unlink()
        build(self.root)
        self.assertFalse((public / "methods" / self.draft.stem).exists())

    def test_draft_in_public_sources_fails_and_preserves_last_build(self):
        public, _ = build(self.root)
        original = (public / "index.html").read_bytes()
        shutil.copyfile(self.draft, self.root / "content" / "methods" / self.draft.name)
        with self.assertRaisesRegex(ValueError, "Allowed status"):
            build(self.root)
        self.assertEqual((public / "index.html").read_bytes(), original)

    def test_canonical_only_on_explicit_production_build(self):
        public, count = build(self.root, production=True)
        self.assertIn(CANONICAL + "/sitemap.xml", (public / "robots.txt").read_text())
        urls = [n.text for n in ET.parse(public / "sitemap.xml").getroot().iter() if n.tag.endswith("}loc")]
        self.assertEqual(len(urls), count - 1)
        self.assertTrue(all(url.startswith(CANONICAL + "/") for url in urls))
        self.assertIn(f'rel="canonical" href="{CANONICAL}/methods/"', (public / "methods/index.html").read_text())
        self.assertNotIn("noindex", (public / "index.html").read_text())
        self.assertIn("noindex", (public / "404.html").read_text())
        build(self.root)
        self.assertFalse((public / "sitemap.xml").exists())
        self.assertNotIn('rel="canonical"', (public / "index.html").read_text())

    def test_declines_review_in_repo_and_review_in_production(self):
        for folder, release in [(self.root / "content", False), (self.drafts, True)]:
            with self.assertRaises(ValueError):
                build(self.root, folder, release)

    def test_broken_fragment_fails(self):
        public, _ = build(self.root)
        home = public / "index.html"
        home.write_text(home.read_text().replace('href="#agenda"', 'href="#missing"'))
        with self.assertRaisesRegex(ValueError, "Missing anchor"):
            audit(public)

    def test_supported_markdown_is_escaped_and_anchored(self):
        output, headings = markdown("## One\n\n## One\n\n<strong> & **bold**\n\n- first\n- second")
        self.assertIn("&lt;strong&gt; &amp; <strong>bold</strong>", output)
        self.assertIn("<li>second</li>", output)
        self.assertEqual([h[0] for h in headings], ["one", "one-2"])


if __name__ == "__main__":
    unittest.main()
