import sc_edit as e


PARAGRAPH = "South Carolina law states that, upon conviction for selling alcohol to a person under 21, the person who made the sale is guilty of a misdemeanor and must be fined between $200 and $300 or imprisoned for up to 30 days, or both, for a first offense. For a second or subsequent offense, the person must be fined between $400 and $500 or imprisoned for up to 30 days, or both. The same consequence structure applies to unlawful transfer of beer, wine, or liquor to a person under 21 for consumption."


data = e.load()
s3 = e.section(data, 3)

anchor = e.find_first(s3, "Selling alcohol to someone under 21 is a misdemeanor")
if anchor == -1:
    anchor = e.find_first(s3, "prima facie")
if anchor == -1:
    anchor = 10

e.insert_after(s3, anchor, [e.make_text([PARAGRAPH])])
e.reflow(s3)
e.save(data)
