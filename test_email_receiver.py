import email_receiver as er

def test_bad_email_connect():
    mail_box = "gomromgolovin3@gmail.com"
    password = "lodaezfcwhgdjxux"
    res = er.connect(mail_box, password)
    if res == 0:
        print("TEST BAD EMAIL PASSED!")
    else: print("TEST BAD EMAIL FAILED!")

def test_email_connect():
    mail_box = "romgolovin3@gmail.com"
    password = "lodaezfcwhgdjxux"
    res = er.connect(mail_box, password)
    if res != 0:
        print("TEST EMAIL PASSED!")
    else: print("TEST EMAIL FAILED!")

def test_send_and_receive_mail():
    subject = "casp-meta"
    msg_body = """
    TARGET=T1112
SEQUENCE=MGETKKMICLVDGEHYFPVVKDSIEILDDLEHIDVVAVVFIGGTEKLQIEDPKEYSEKLGKPVFFGPDPKKIPYDVIKKCVKKYNADIVMDLSDEPVVDYTKRFRIASIVLKEGAVYQGADFKFEPLTEYDVLEKPSIKIIGTGKRIGKTAVSAYAARVIHKHKYNPCVVAMGRGGPREPEIVEGNKIEITAEYLLEQADKGVHAASDHWEDALMSRILTVGCRRCGGGMLGDTFITNVKRGAEIANKLDSDFVIMEGSGAAIPPVKTNRQIVTVGANQPMININNFFGPFRIGLADLVIITMCEEPMATTEKIKKVEKFIKEINPSANVIPTVFRPKPVGNVEGKKVLFATTAPKVVVGKLVNYLESKYGCDVVGVTPHLSNRPLLRRDLKKYINKADLMLTELKAAAVDVATRVAIEAGLDVVYCDNIPVVIDESYGNIDDAIIEVVEMAIDDFKNNR
REPLY-E-MAIL=models@predictioncenter.org 
               """
    er.send_mail(subject, msg_body)
    mail, data = er.get_mail(True, subject)
    size = len(list(data.values()))
    if size > 0:
      for data in list(data.values()):
        target = data.split('\r')[0].split('=')[1]
        sequence = data.split('\r')[1].split('=')[1]
        unprocessed_seq = data.split('\r')[1:]
        seq = ''
        for section in unprocessed_seq:
          if '\n' in section:
            section = section.replace('\n','')
          if '=' in section:
            section = section.replace('=','')
          seq += section
        reply_email_index = seq.index("REPLY-E-MAIL")
        sequence = seq[:reply_email_index].replace('SEQUENCE3D','')
        target = target[2:]
    else: print("TEST FAILED! NO MAIL RECEIVED!")

if __name__ == "__main__":
    test_bad_email_connect()
    test_email_connect()
    test_send_and_receive_mail()
