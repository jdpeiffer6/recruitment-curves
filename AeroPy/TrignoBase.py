"""
This class creates an instance of the Trigno base. Put in your key and license here
"""
import clr
clr.AddReference("/resources/DelsysAPI")
clr.AddReference("System.Collections")


from Aero import AeroPy

key = "MIIBKjCB4wYHKoZIzj0CATCB1wIBATAsBgcqhkjOPQEBAiEA/////wAAAAEAAAAAAAAAAAAAAAD///////////////8wWwQg/////wAAAAEAAAAAAAAAAAAAAAD///////////////wEIFrGNdiqOpPns+u9VXaYhrxlHQawzFOw9jvOPD4n0mBLAxUAxJ02CIbnBJNqZnjhE50mt4GffpAEIQNrF9Hy4SxCR/i85uVjpEDydwN9gS3rM6D0oTlF2JjClgIhAP////8AAAAA//////////+85vqtpxeehPO5ysL8YyVRAgEBA0IABGss/cHpafl/kdAPODaITYOw7WcaYR5YDwkkEMFQiCk2qK+0AP0x+t7/QjJybHHlP5HkRlkua4mBTg8NgUkEeLY="
license = "<License>"\
  "<Id>0b132674-fc99-4de9-9286-208b3596b2c4</Id>"\
  "<Type>Standard</Type>"\
  "<Quantity>10</Quantity>"\
  "<LicenseAttributes>"\
  "<Attribute name=\"Software\">VS2012</Attribute>"\
  "</LicenseAttributes>"\
  "<ProductFeatures>"\
  "<Feature name=\"Sales\">True</Feature>"\
  "<Feature name=\"Billing\">False</Feature>"\
  "</ProductFeatures>"\
  "<Customer>"\
  "<Name>JD Peiffer</Name>"\
  "<Email>j.d@wustl.edu</Email>"\
  "</Customer>"\
  "<Expiration>Tue, 21 Oct 2025 04:00:00 GMT</Expiration>"\
  "<Signature>MEQCICynJG9F/+9nKR2jejwcB2WFrYZcvI+qJaKE//phF9KmAiBRichFb76wgGhrwGgcj/UFek0RhMZGEWsOaqucul6EHA==</Signature>"\
  "</License>"\

class TrignoBase():
    def __init__(self):
        self.BaseInstance = AeroPy()