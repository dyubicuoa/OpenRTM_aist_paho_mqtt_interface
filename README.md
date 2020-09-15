# OpenRTM-aist Python用 Paho MQTT通信モジュール

本ソフトウェアはロボットミドルウェアの一つであるRTミドルウェアで構築されたロボットシステムにおいて、MQTT（Message Queuing Telemetry Transport）プロトコルによる通信を実現する産業技術総合研究所開発のOpenRTM-aist Python用拡張モジュール群です。  
OpenRTM-aistを本モジュール群で拡張することで、RTコンポーネントのデータポートのInterface TypeにMQTTを追加することができます。Interface TypeとしてMQTTを選択することでデータポート間の通信をMQTTで行えるようになります。  

![top01](https://user-images.githubusercontent.com/40682353/93169044-36b4e500-f75f-11ea-9bce-aa67e1d98ec4.png)

## Target users
* OpenRTM-aistのユーザでMQTTの初学者が、RTシステムを通してMQTTによる通信システムを試しに体験してみたい方
* OpenRTM-aistを用いて手軽にインターネット上のシステム、すなわちIoT（Internet of Things）システムやロボットシステムのインターネット化であるIoRT（Internet of Robotic Things）システムを構築したい方
 
## Features

MQTT通信モジュールは以下の4種類で構成されています。

|| MQTT通信モジュール名 | Interface Type | 説明 |
| :-- | :-- | :-- | :-- |
| (1) | **OutPortPahoPublisher** | 'paho_mqtt' | OutPort用MQTTデータ送信モジュール。セキュア通信機能なし |
| (2) | **InPortPahoSubscriber** | 'paho_mqtt' | InPort用MQTTデータ受信モジュール。セキュア通信機能なし |
| (3) | **OutPortPahoPubSecure** | 'paho_mqtts' | OutPort用MQTTデータ送信モジュール。TLSによるセキュア通信機能付き |
| (4) | **InPortPahoSubSecure** | 'paho_mqtts' | InPort用MQTTデータ受信モジュール。TLSによるセキュア通信機能付き|

いずれの通信モジュールもVersion3.1.1のMQTTを扱ってます。(1)および(2)はセキュア通信機能がないため、ローカルマシン内やローカルネットワーク内での通信用途限定です。インターネット上でシステムを構築する場合はセキュア通信機能付きの(3)および(4)を使用してください。  

各通信モジュールのプロパティとそのdefault値は以下のとおりです。

**(1) OutPortPahoPublisher** および **(2) InPortPahoSubscriber**  
||Name (Key)|Default value| 説明 |
| :-- | :-- | :-- | :-- |
| 1. | host | 'localhost' | エンドポイントとなるBrokerのアドレス（FQDNまたはIPアドレス） |
| 2. | port | 1883 | MQTTメッセージングサービスのポート番号 |
| 3. | kpalv | 60 | コネクション維持のための指標。単位はsで、設定時間内に通信が確認できなければ自動的にコネクションが破棄される |
| 4. | topic | 'test' | メッセージンググループ名。メッセージの送受信を行うクライアントは同一のTopicに属していなければいけない |
| 5. | qos | 0 | メッセージング品質。MQTTでは0, 1, 2の何れかから選択する。数字が大きいほど高品質だが処理的に重くなる |
| 6. | id | None | クライアントID。Brokerに対してuniqueな値でなければいけない。defaultでは乱数により値が与えられる |
| 7. | cs | True | Clean Session。クライアントの接続が切れた場合に、Brokerで接続時のSession情報を残しておくか否か |

**(3) OutPortPahoPubSecure** および **(4) InPortPahoSubSecure**  
||Name (Key)|Default value| 説明 |
| :-- | :-- | :-- | :-- |
| 1. | host | 'localhost' | エンドポイントとなるBrokerのアドレス（FQDNまたはIPアドレス） |
| 2. | port | 8883 | MQTTS（MQTT Secure）メッセージングサービスのポート番号 |
| 3. | kpalv | 60 | コネクション維持のための指標。単位はsで、設定時間内に通信が確認できなければ自動的にコネクションが破棄される |
| 4. | topic | 'test' | メッセージンググループ名。メッセージの送受信を行うクライアントは同一のTopicに属していなければいけない |
| 5. | qos | 0 | メッセージング品質。MQTTでは0, 1, 2の何れかから選択する。数字が大きいほど高品質だが処理的に重くなる |
| 6. | id | None | クライアントID。Brokerに対してuniqueな値でなければいけない。defaultでは乱数により値が与えられる |
| 7. | cs | True | Clean Session。クライアントの接続が切れた場合に、Brokerで接続時のSession情報を残しておくか否か |
| 8. | cacert | './ca.crt' | 認証局（Certificate Authority）証明書へのpath。サーバの真正性を証明するのに必要 |
| 9. | cltcert | './client.crt' | クライアント証明書へのpath。クライアントの真正性を証明するのに必要 |
| 10. | cltkey | './client.key' | クライアント秘密鍵へのpath。クライアントの真正性を証明するのに必要 |

プロパティは以下のようにRTSystemEditor上でRTコンポーネントにおけるデータポートの接続を行う際に表示されるConnector Profileダイアログの"詳細"からKey-Value形式で入力することができます。Keyは必ずしも上記の順番で入力する必要はありません。いくつかのKeyを選択し、順不同で入力することができます。

![features01](https://user-images.githubusercontent.com/40682353/93169151-6fed5500-f75f-11ea-957e-ab352e508656.png)

## Requirement
 
MQTT通信モジュールをインストールし使用するにはPython版OpenRTM-aistおよびMQTTクライアントライブラリpahoが必要になります。
 
* OpenRTM-aist-Python 1.1.x or 1.2.x
* paho-mqtt

実際にRTコンポーネントのデータポート間でMQTTによる通信を行うにはいずれかのMQTT Brokerが必要となります。もしオンライン上のIoTプラットフォーム等外部のメッセージングサービスを利用せずに、自身で用意する場合は、予めOSSのBrokerソフトウェアをインストールしてください。なお、本通信モジュールはEclipse Mosquittoでの動作確認を行っています。

 
## Installation

以降はUbuntuまたはdebianディストリビューションでのインストレーションを想定しています。

### ver.1.2.2以降のOpenRTM-aist（python3系）を使用している場合のインストール方法

(1) OpenRTM-aist-Pythonのインストール方法は産業技術総合研究所のOpenRTM-aistオフィシャルWebサイトを参照してください。ここでは割愛します。

(2) MQTTクライアントライブラリpaho-mqttのインストール。インストール済みであれば省略
```bash
$ sudo pip3 install paho-mqtt
```

(3) 必要であればいずれかのBrokerソフトウェアをインストール。以下はEclipse Mosquittoをインストールする場合。必要なければ省略
```bash
$ sudo apt install mosquitto
```

(4) githubのリポジトリからMQTT通信モジュールに関連するファイル群をcloneし、MQTT通信モジュール群をインストール。なお、アンインストールは`sudo pip uninstall OpenRTM_aist_paho_mqtt_module`で行えます。
```bash
$ cd ~/
$ git clone https://github.com/dyubicuoa/OpenRTM_aist_paho_mqtt_interface
$ cd OpenRTM_aist_paho_mqtt_interface/OpenRTM_aist_v122l_paho_mqtt_module
$ sudo pip3 install .
```

### ver.1.2.1以前のOpenRTM-aist（python2系）を使用している場合のインストール方法

(1) OpenRTM-aist-Pythonのインストール方法は産業技術総合研究所のOpenRTM-aistオフィシャルWebサイトを参照してください。ここでは割愛します。

(2) MQTTクライアントライブラリpaho-mqttのインストール。インストール済みであれば省略
```bash
$ sudo pip install paho-mqtt
```

(3) 必要であればいずれかのBrokerソフトウェアをインストール。以下はEclipse Mosquittoをインストールする場合。必要なければ省略
```bash
$ sudo apt install mosquitto
```

(4) githubのリポジトリからMQTT通信モジュールに関連するファイル群をcloneし、MQTT通信モジュール群をインストール。なお、アンインストールは`sudo pip uninstall OpenRTM_aist_paho_mqtt_module`で行えます。
```bash
$ cd ~/
$ git clone https://github.com/dyubicuoa/OpenRTM_aist_paho_mqtt_interface
$ cd OpenRTM_aist_paho_mqtt_interface/OpenRTM_aist_v121e_paho_mqtt_module
$ sudo pip install .
```

## Usage

以下では、Linux（Ubuntu or Debian）の環境下において、OpenRTM-aist上のMQTT通信インタフェースを利用してロボットシステムを構築する手順を示します。構築例で使用するのはOpenRTM-aistで予めexampleとして用意されているConsoleInとConsoleOutの各コンポーネントですが、当然ながらエンドユーザが独自に開発したRTコンポーネントにも応用可能です。

### (1) rtc.confでのモジュール指定
MQTT通信モジュールをOpenRTM-aistに組み込むには、MQTTで通信を行いたいRTコンポーネントのコンフィギュレーションファイル"rtc.conf"において、MQTT通信モジュールへのpathとモジュール名を指定する必要があります。OutPortはデータを送信する側なので、OutPortPahoPublisherもしくはOutPortPahoPubSecureのいずれかのMQTT Publisher通信モジュールを指定します。一方、InPortはデータを受信する側なので、OutPortPahoSubscriberもしくはOutPortPahoSubSecureのいずれかのMQTT Subscriber通信モジュールを指定します。

例えば、セキュア通信機能なしのMQTT通信インタフェースを用いてOutPortからデータを送信したい場合は以下のようにrtc.confに記述します。
```bash
# rtcPub.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPublisher.py
```

セキュア通信機能なしのMQTT通信インタフェースを用いてInPortにてデータを受信したい場合は以下の通り。
```bash
# rtcSub.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: InPortPahoSubscriber.py
```

一つのRTコンポーネントにOutPortもInPortも備わっており、そのどちらもセキュア通信機能付きのMQTT通信インタフェースを通してデータの送受信を行いたい場合は以下のように","で区切ってモジュール名を2つ指定します。
```bash
# rtcPubSubSecure.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPubSecure.py, InPortPahoSubSecure.py
```

MQTT通信モジュールのインストール先は、`pip show OpenRTM_aist_paho_mqtt_module`で確認できます。なお、インストール後はインストール先のモジュールではなく、cloneしたレポジトリ内にあるモジュールを指定しても構いません。"rtc.conf"の設定例はリポジトリの"OpenRTM_aist_paho_mqtt_module/samples/rtc_conf/"配下に置いてあるので参考にしてください。

### (2) MQTT Brokerの稼働状況確認
RTコンポーネント実行前にMQTT Brokerが稼働中であることを確認してください。特にBrokerソフトウェアインストール直後は稼働していない場合が多いです。

以下はMosquittoの稼働状況から、inactiveであることを確認した上でBrokerによるメッセージングサービスをバックグラウンドプロセスとしてスタートさせる例です。
```bash
$ sudo systemctl status mosquitto.service
service 
● mosquitto.service - Mosquitto MQTT Broker
   Loaded: loaded (/lib/systemd/system/mosquitto.service; disabled; vendor prese
   Active: inactive (dead)
     Docs: man:mosquitto.conf(5)
           man:mosquitto(8)

$ sudo systemctl start mosquitto.service
```

### (3) RTコンポーネントの実行
(1)で設定したrtc.confをオプションで指定し、ターゲットとなるRTコンポーネントを実行します。

以下はConsoleInとConsoleOutの各コンポーネントの実行例です。ConsoleInはOutPortを備えているのでrtcPub.confを、ConsoleOutはInPortを備えているのでrtcSub.confをそれぞれオプションとして指定します。
```bash
$ python ConsoleIn.py -f rtcPub.conf
```
```bash
$ python ConsoleOut.py -f rtcSub.conf
```

### (4) データポートとBrokerの接続
![usage01](https://user-images.githubusercontent.com/40682353/93169247-aa56f200-f75f-11ea-9cf0-c38fff156859.png)

OpenRTPを起動し、RTSystemEditorのSystem Diagramに先ほど実行したRTコンポーネントをセットします。

![usage02](https://user-images.githubusercontent.com/40682353/93169326-d4a8af80-f75f-11ea-845a-9a0dc91d97df.png)

データ送信側RTコンポーネントConsoleInのOutPortを右クリックし、"接続"を選択します。

![usage03](https://user-images.githubusercontent.com/40682353/93169366-e68a5280-f75f-11ea-9762-409585f32a36.png)

Connector Profileダイアログが立ち上がるのでProfile中の【Interface Type】から"paho_mqtt"を選択します。これで通信インタフェースがCORBAからMQTTへと切り替わります。

![usage04](https://user-images.githubusercontent.com/40682353/93169383-f144e780-f75f-11ea-986a-204dcffbfa70.png)

MQTT通信モジュールのプロパティをdefaultのまま使用する場合は右下の"OK"ボタンをクリックすることでdefaultの情報でMQTT Brokerへの接続が行われます。OutPortが緑色になればBrokerへの接続完了です。MQTT通信モジュールのプロパティを変更したい場合は、モジュールに渡すプロパティを設定するため、左下の"詳細"をチェックします。

![usage05](https://user-images.githubusercontent.com/40682353/93169411-00c43080-f760-11ea-8c75-15cb1404761b.png)

Connector ProfileダイアログにBufferの各種設定と、MQTT通信モジュールのプロパティ設定を行えるダイアログが追加表示されます。最下部の"Name"および"Value"と表示されている部分がプロパティ設定箇所です。右横の"追加"ボタンをクリックします。

![usage06](https://user-images.githubusercontent.com/40682353/93169432-0caff280-f760-11ea-8dde-0206c82b1246.png)

プロパティの設定箇所が追加されます。複数のプロパティを変更する場合は必要分"追加"ボタンをクリックしてください。プロパティはNameとValueの組み合わせ、すなわちkey-value型で設定できます。Featuresで示した設定可能なプロパティを確認しながら、変更が必要なプロパティを入力します。例えばMQTT BrokerのアドレスとTopic名を変更したい場合は次のように入力します。なお、Brokerの設定次第では使用可能なTopicが制限されていることもあるのでサーバの管理者に、クライアント側でTopicを設定可能かどうか予め確認しておきましょう。

![usage07](https://user-images.githubusercontent.com/40682353/93169451-16d1f100-f760-11ea-8827-f1b011ce4bd8.png)

プロパティ設定後、右下の"OK"ボタンをクリックすれば、入力したプロパティがMQTT通信モジュールに反映され、更新された情報を元にMQTT Brokerへの接続が行われます。

![usage08](https://user-images.githubusercontent.com/40682353/93169472-20f3ef80-f760-11ea-88af-32beee2dcf1e.png)

このように、MQTT通信インタフェースを用いた場合はデータポート単体でBrokerに接続する形をとります。このため、データポート間での結線は行いません。なぜならばMQTTにおけるPublisher（送信者）とSubscriber（受信者）の各クライアントの接続先はサーバとなるBrokerであり、お互いに直接的に接続する通信アーキテクチャとはなっていないためです。BrokerはRTSystemEditor上では表示されませんが、データポートが緑色に変わればBrokerへの接続は成功しています。

![usage09](https://user-images.githubusercontent.com/40682353/93169504-2d784800-f760-11ea-9b64-49ad91b6675c.png)

データ受信側RTコンポーネントConsoleOutも同じ要領で、InPort右クリックからConnector Profileの設定を行い、MQTT Brokerに単体で接続します。その後、通常通りそれぞれのRTコンポーネントをAvtivate化することでRTシステムが稼働します。

## Note

### データポート間の結線について
MQTT通信インタフェースはデータポート右クリックでの接続が基本です。データポート間の結線によるBrokerへの接続も可能ですが、できるだけ行わないでください。どうしても結線したい場合はプロパティのClient IDはバッティングを避けるため、デフォルトのランダム値を使用するようにしてください。また、1対Nで結線する場合、例えばOutPort一つに対して複数のInPortをすべて結線でBrokerに接続しようとすると、OutPort側の通信モジュールのインスタンスが複数立ち上がるため、メッセージングが多重化してしまい想定通りの通信ができなくなりますので気をつけてください。

### 動作確認済みの環境
* Ubuntu 16.04 x86-64 CPU
* Ubuntu 18.04 x86-64 CPU
 
## Author

* 吉野 大志 (Daishi Yoshino)
* 会津大学 復興支援センター (Revitalization center, University of Aizu)
* FB: https://www.facebook.com/daishi.y.uoa
 
## License
 
"OpenRTM-aist Python用 Paho MQTT通信モジュール" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
