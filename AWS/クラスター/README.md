### 概要
<br>
AWS ECS（Amazon Elastic Container Service） は、DockerコンテナなどをAWS上で実行・管理するためのフルマネージドなコンテナオーケストレーションサービスである。

コンテナオーケストレーションサービスとは、多数のコンテナを自動で配置・起動・停止・監視・スケールしてくれる管理サービスである。<br>

■ECSを構成する主なコンポーネント<br>

![ECS 04](./ECS_04.png)
<br>
■起動タイプの選択　(ECSを構成する2つの起動タイプについて)<br><br>

![ECS 05](./ECS_05.png)
<br>
<br>
<br>
### 作成イメージ
<br>
・最小限な構成でECSを使用する。<br>
・Nginx用のコンテナをダウンロードして、それをデプロイする。<br>
・VPC内のpublic subnetの中にECSを通じてnginxのコンテナをデプロイする。<br>
・起動タイプはfargateを使用する。<br>
・コンテナにpublic IPを付与する。<br>
※ECRを使用しない。<br><br>
![ECS 03](./ECS_03.png)

成功：

public IPを通じてNginxの画面が表示される。




