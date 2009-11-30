import email.Message

from collective.testcaselayer import ptc as tcl_ptc

from Products.MailHost import interfaces
from Products.SecureMailHost import SecureMailHost

class MockMailHost(SecureMailHost.SecureMailHost):
    
    def __init__(self, id):
        super(MockMailHost, self).__init__(id, smtp_notls=True)
        self.reset()
    
    def reset(self):
        self.messages = []
        self._p_changed = True

    def _send(self, mfrom, mto, messageText, debug=False):
        if not isinstance(messageText, email.Message.Message):
            message = email.message_from_string(messageText)
        else:
            message = messageText
        self.messages.append(message)
        self._p_changed = True
    
    def pop(self, idx=-1):
        result = self.messages.pop(idx)
        self._p_changed = True
        return result

    def __len__(self):
        return len(self.messages)

class MockMailHostLayer(tcl_ptc.BasePTCLayer):
    """Use the mock mail host"""

    def afterSetUp(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mh = MockMailHost('MailHost')
        self.portal.getSiteManager().registerUtility(
            mh, interfaces.IMailHost)

mockmailhost_layer = MockMailHostLayer([tcl_ptc.ptc_layer])
