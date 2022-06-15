import paramiko
import re

host = "132.72.44.112"
targets_path = "/home/keasar/casp15/programs/amor/tmp_targets" #TODO - change to the real targets folder
username = "omerkemp"
ssh_key_path = "/users/studs/bsc/2016/orelhaz/.ssh/id_rsa"


class ShellHandler:

    def __init__(self, host, user):
        k = paramiko.RSAKey.from_private_key_file(ssh_key_path)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host, username=user, pkey=k, port=22)

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def cp(self, localfilepath, remotefilepath):
        ftp_client = self.ssh.open_sftp()
        ftp_client.put(localfilepath, remotefilepath)
        ftp_client.close()

    def execute(self, cmd):
        """

        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                # up for now filled with shell junk from stdin
                shout = []
            elif str(line).startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap sherr with shout in a case of failure.
                    sherr = shout
                    shout = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        # first and last lines of shout/sherr contain a prompt
        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)

        return shin, shout, sherr




def create_new_target(target, sequence):
    sh = ShellHandler(host, username)
    shin, shout, sherr = sh.execute("cd " + targets_path)
    print(sherr)
    shin, shout, sherr = sh.execute("mkdir " + target)
    print(sherr)
    f_path = target + ".fasta"
    f = open(f_path, 'w')
    f.truncate(0)
    content = ">"+target+"\n"+sequence
    f.write(content)
    f.close()
    sh.cp(f_path, targets_path + "/" + target + "/" + f_path)
    

def delete_target(targetName):
    sh = ShellHandler(host, username)
    delete_file_path = "/home/keasar/casp15/programs/amor/meshi_shell"
    shin, shout, sherr = sh.execute("cd " + delete_file_path)
    print(sherr)
    print(shout)
    if sherr == []:
        shin, shout, sherr = sh.execute("python3 deleteFromDB.py " + targetName)
    print(shout)
    print(sherr)

if __name__ == '__main__':
    create_new_target("T1095556",
                      "MDILENYVSFDEQARDINIAFDKLFGRDDISHMNNFSINKRSYYNCLDQISDDLNLVLNKYNDLAYSLLEIRYNMATKENYTHMEFYSDIERLFIKNEKLLNVISDIVEEEYDLDLNQASKGKKINIELQVTDNLNKIYLKSSVLMRILIPILCDFNCDDDINEVLVYDIFKEVIKSFDDGKKNALNKLYKIIYSRVFETKYSDVVIWTYLKNMSTDLMIIVKDYFKVIIKKIFPKLKHNSSVISYLDVVIKQKLKYLFTFKYPISYKPLKAETTDDEELSEQERMEINLLRNDQGNSIINECSIKQEIAKIKKKYNVTDEVMKEFINGRELNSIQIYLVKIYYSNKFKVNSNKNDIFYLLYGMTRELGEMNFSIIPEILSCAIAPNVRKMNNRKKLVDKIIHSDKYSYLLKSYLPIKNILDKNNVILQLMTIKNAKFMNKENKEVDFSTDHLAEEVLDMLLCI")
   # delete_target("T1095555")
