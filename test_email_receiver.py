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
    subject = "Protein Structure Query"
    msg_body = "TARGET=TEST_SEQUENCE_1\r\n" \
               "SEQUENCE=TEST_MDILENYVSFDEQARDINIAFDKLFGRDDISHMNNFSINKRSYYNCLDQISDDLNLVLNKYNDLAYSLLEIRYNMATKENYTHMEFYSDIERLFIKNEKLLNVISDIVEEEYDLDLNQASKGKKINIELQVTDNLNKIYLKSSVLMRILIPILCDFNCDDDINEVLVYDIFKEVIKSFDDGKKNALNKLYKIIYSRVFETKYSDVVIWTYLKNMSTDLMIIVKDYFKVIIKKIFPKLKHNSSVISYLDVVIKQKLKYLFTFKYPISYKPLKAETTDDEELSEQERMEINLLRNDQGNSIINECSIKQEIAKIKKKYNVTDEVMKEFINGRELNSIQIYLVKIYYSNKFKVNSNKNDIFYLLYGMTRELGEMNFSIIPEILSCAIAPNVRKMNNRKKLVDKIIHSDKYSYLLKSYLPIKNILDKNNVILQLMTIKNAKFMNKENKEVDFSTDHLAEEVLDMLLCI"
    er.send_mail(subject, msg_body)
    mail, data = er.get_mail(True, subject)
    size = len(list(data.values()))
    if size > 0:
        target = list(data.values())[size-1].split('\r')[0].split('=')[1]
        sequence = list(data.values())[size-1].split('\r')[1].split('=')[1]
        print("MAIL SENT AND RECEIVED SUCCESSFULLY!")
        print("Target received: " + target)
        print("Sequence received: " + sequence)
    else: print("TEST FAILED! NO MAIL RECEIVED!")

if __name__ == "__main__":
    test_bad_email_connect()
    test_email_connect()
    test_send_and_receive_mail()