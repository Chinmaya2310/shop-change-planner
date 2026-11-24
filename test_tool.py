"""Rows here are made up for testing only. Real rows are in data.csv."""
import contextlib, io, os, tempfile, unittest
import tool

HEAD = "id,date,time,amount,notes\n"
GOOD = "".join(f"{i},2020-01-01,10:00,{40+i},\n" for i in range(1, 21))

class T(unittest.TestCase):
    def run_tool(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "d.csv")
            with open(p, "w") as f: f.write(text)
            out = io.StringIO()
            with contextlib.redirect_stdout(out): code = tool.main(p)
        return code, out.getvalue()

    def test_change(self):
        self.assertEqual(tool.make_change(53), {50: 1, 2: 1, 1: 1})
        self.assertEqual(tool.handed_over(520, 500), 1000)
        self.assertEqual(tool.handed_over(50, 50), 50)

    def test_good(self):
        code, out = self.run_tool(HEAD + GOOD)
        self.assertEqual(code, 0)
        self.assertIn("Keep ready:", out)

    def test_bad_rows(self):
        for row, why in [("1,2020-01-01,10:00,9,", "duplicate id"), (",2020-01-01,10:00,9,", "blank id"),
                         ("99,2020-13-01,10:00,9,", "bad date"), ("99,2999-01-01,10:00,9,", "future"),
                         ("99,2020-01-01,10:00,x,", "whole number"), ("99,2020-01-01,10:00,,", "whole number"),
                         ("99,2020-01-01,10:00,-4,", "above zero"), ("99,2020-01-01", "columns"),
                         ("99,2020-01-01,10:00,9,,extra", "columns")]:
            with self.subTest(row=row):
                code, out = self.run_tool(HEAD + GOOD + row + "\n")
                self.assertEqual(code, 0)
                self.assertIn(why, out)
                self.assertIn("Skipped line 22", out)

    def test_too_few_empty_missing(self):
        self.assertIn("Need at least", self.run_tool(HEAD)[1])
        self.assertIn("missing columns", self.run_tool("")[1])
        with contextlib.redirect_stdout(io.StringIO()) as o:
            self.assertEqual(tool.main("/nonexistent.csv"), 1)
        self.assertIn("Cannot read", o.getvalue())

unittest.main()
