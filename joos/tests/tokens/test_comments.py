from joos.tokens.comments import *


class TestComments(object):
    def test_traditional_comment(self):
        re = comment
        assert re.ShouldAccept("""/** this is a javadoc comment*/""")
        assert re.ShouldAccept("""/* this comment\r\n// * / end here */""")
        assert not re.ShouldAccept("""/** * asdf*""")
        assert not re.ShouldAccept("""**asdf*/""")

    def test_end_of_line_comment(self):
        re = comment
        assert re.ShouldAccept("""//** this is an end of line\r\n""")
        assert re.ShouldAccept("""// yup\n""")
        assert not re.ShouldAccept("""// this comment missing newline""")
        assert not re.ShouldAccept("""not comment\r\n""")
