# GitHubリポジトリにコードをpushする

##	準備

(1)	GitHub上でPrivate リポジトリを作成する。

 ![CI CD](./CD CD01_01.png)
 
(2)	GitHub上でコードをプッシュするためのカギを作成する。

※Settings →　Developer Settings　 →　Personal access tokens (classic)

  ![CI/CD](./CD CD01_02.png)

(3)	鍵の名前、使用期間、スコープにレジストリーを選択し、作成する。
 
 ![CI/CD](./CD CD01_03.png)
 
(4)	鍵のキーを取得する。

 ![CI/CD](./CD CD01_04.png)
 
##	GitHubリポジトリにコードをpushする

(1)	Amazon Linux環境にGitをインストールする。※cloud shell上で操作する場合は不要。

コマンド：sudo dnf install git -y

![CI/CD](./CD CD01_05.png) 

(2)	Githubのコードを取得する。

コマンド：git clone https://github.com/<その後のディレクトリ>

![CI/CD](./CD CD01_06.png) 

(3)	Pushする用のファイル(フォルダ)を用意する。

![差し替え予定](./CD CD01_07.png) 


(4)	現在いるディレクトリをGit管理対象にする。

コマンド：git init

※実行すると、そのディレクトリに隠しディレクトリ.gitが作られ、コミット履歴やブランチ情報が保存される。

![CI/CD](./CD CD01_08.png)  

(5)	現在の変更を「次のコミット対象」に登録する。

コマンド：git add -A

git add した変更を、Gitの履歴として保存する。

コマンド：git commit -m "first commit"

現在のブランチ名を main に変更する。

コマンド：git branch -M main

![CI/CD](./CD CD01_09.png) 

(6)	ローカルGitとGitHubリポジトリの「接続先」を登録する。

コマンド：git remote add origin [GitHubのURL]

ローカルの main ブランチの内容を、GitHubの origin にアップロードする。

コマンド：git push -u origin main

　　　※ユーザー名とPersonal access tokens (classic)を入力する。

 ![CI/CD](./CD CD01_10.png) 

(7)	コピー先のGitHubを確認する。

 ![CI/CD](./CD CD01_11.png)  

(8)	画面をリロードする。

![CI/CD](./CD CD01_12.png) 

![差し替え予定](./CD CD01_13.png) 
 
## その他の補足コマンド

・GitHubとの接続先登録

コマンド：git remote -v

![CI/CD](./CD CD01_14.png)   

・Gutのステータスを表示する。

コマンド：git status

![CI/CD](./CD CD01_15.png)  
 
・現在のブランチ → main 

・未コミットの変更 → なし 

・作業ツリー → クリーン

・Gitのログを表示する

コマンド：git log --oneline

![CI/CD](./CD CD01_16.png)  
 
