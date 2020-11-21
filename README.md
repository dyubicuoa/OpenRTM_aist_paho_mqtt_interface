# OpenRTM-aist Python用 Paho MQTT通信モジュール

本ソフトウェアはロボットミドルウェアの一つであるRTミドルウェアで構築されたロボットシステムにおいて、**MQTT（Message Queuing Telemetry Transport）プロトコル**による通信を実現する産業技術総合研究所開発のOpenRTM-aist Python用拡張モジュール群です。  

OpenRTM-aistを本モジュール群で拡張することで、RTコンポーネントのデータポートのInterface TypeにMQTTを追加することができます。通常OpenRTM-aistではInterface TypeとしてCORBAが利用されますが、通信インタフェースとして追加されたMQTTを選択することでデータポート間の通信をMQTTで行えるようになります。

つまり、OpenRTM-aistのユーザは、これまでと同様にRTコンポーネントを開発、実行し、RTSystemEditor等でRTシステムを構築する感覚で、IoTシステムを構築できるのです。MQTT通信インタフェースを利用するのに必要な過程は、rtc.confやRTSystemEditorにてMQTT通信モジュールや関連するプロパティを指定するだけです。

MQTT通信モジュールを通して、IoTシステム構築ミドルウェアとしてのOpenRTM-aistに触れてみてください。

<img src="https://user-images.githubusercontent.com/40682353/93169044-36b4e500-f75f-11ea-9bce-aa67e1d98ec4.png" width=70%>

## Target users
* OpenRTM-aistのユーザでMQTTの初学者が、RTシステムを通してMQTTによる通信システムを試しに体験してみたい方
* OpenRTM-aistを用いて手軽にインターネット上のシステム、すなわちIoT（Internet of Things）システムやロボットシステムのインターネット化であるIoRT（Internet of Robotic Things）システムを構築したい方
* OpenRTM-aistで構築したRTシステムと、MQTTクライアントライブラリから構築した外部のMQTTシステムや、AWS等が提供するクラウドサービスと連携を取りたい方

## Directory structure
リポジトリのフォルダ構成は以下の通り。

```bash
OpenRTM_aist_paho_mqtt_interface
|  README.md
|  CHANGELOG.md
|  LICENSE
|
└--OpenRTM_aist_v121e_paho_mqtt_interface
|  └--OpenRTM-aist ver.1.2.1以前（Python2系）用のMQTT通信モジュール群
|
└--OpenRTM_aist_v122l_paho_mqtt_interface
|  └--OpenRTM-aist ver.1.2.2以降（Python3系）用のMQTT通信モジュール群
|
└--samples
   └--launch_scripts
   |  └--OpenRTM-aistのExample RTC（SeqIO, SimpleIO, Slider_and_Motor）の起動スクリプト
   |
   └--rtc_conf
      └--rtc.confの設定例ファイル群
```

## Features

MQTT通信モジュールは以下の8つで構成されており、メッセージ中のPayloadのシリアライズ形式の違いから、大きくCDRシリアライズ版モジュールとJSONシリアライズ版モジュールの２種類に大別できます。それぞれ異なるPayloadシリアライズ形式を採用しているため、CDRシリアライズ版モジュール間、もしくはJSONシリアライズ版モジュール間でのみMQTT通信が成立します。このことから、CDRシリアライズ版モジュールとJSONシリアライズ版モジュール間の通信はできませんのでご注意ください。

なお、通信モジュールにおける'Interface Type'とは、ロボットシステムを構成するRTコンポーネントのデータポート上で認識される通信インタフェース名を示しています。OpenRTM-aistにおけるInterface Typeのdefaultは'corba_cdr'ですが、下記MQTT用の通信インタフェース名を選択することで、データポートの通信をCORBAからMQTTに変えることが可能となります。

**CDRシリアライズ版MQTT通信モジュール（全データ型に対応）**
|| MQTT通信モジュール名 | Interface Type | 説明 |
| :-- | :-- | :-- | :-- |
| (1) | **OutPortPahoPublisher** | 'mqtt_cdr' | OutPort用MQTTデータ送信モジュール。セキュア通信機能なし |
| (2) | **InPortPahoSubscriber** | 'mqtt_cdr' | InPort用MQTTデータ受信モジュール。セキュア通信機能なし |
| (3) | **OutPortPahoPubSecure** | 'mqtts_cdr' | OutPort用MQTTデータ送信モジュール。TLSによるセキュア通信機能付き |
| (4) | **InPortPahoSubSecure** | 'mqtts_cdr' | InPort用MQTTデータ受信モジュール。TLSによるセキュア通信機能付き|

**JSONシリアライズ版MQTT通信モジュール（BasicDataTypesとExtendedDataTypesのみに対応）**
|| MQTT通信モジュール名 | Interface Type | 説明 |
| :-- | :-- | :-- | :-- |
| (5) | **OutPortPahoPubJson** | 'mqtt_json' | OutPort用MQTTデータ送信モジュール。セキュア通信機能なし |
| (6) | **InPortPahoSubJson** | 'mqtt_json' | InPort用MQTTデータ受信モジュール。セキュア通信機能なし |
| (7) | **OutPortPahoPubJsonSecure** | 'mqtts_json' | OutPort用MQTTデータ送信モジュール。TLSによるセキュア通信機能付き |
| (8) | **InPortPahoSubJsonSecure** | 'mqtts_json' | InPort用MQTTデータ受信モジュール。TLSによるセキュア通信機能付き|

CDRシリアライズ版モジュールはOpenRTM-aistにおけるベースのシリアライズ（マーシャル）形式であるCORBA CDR（Common Data Representation）でシリアライズされたデータをそのままPayloadとして用います。CDRシリアライズが採用されている現行の外部システムは稀であることから、CDRシリアライズ版モジュールはRTシステムにおけるデータポート間の通信にしか利用できず、RTシステム外部の一般のMQTTシステムとの連携はできません。しかしながら、RTシステム中のデータポート間の通信においては、データ処理が軽いことから**JSONシリアライズ版モジュールよりも通信上のパフォーマンスは高くなります**。ですので、RTシステム内でMQTT通信が完結するのであれば、CDRシリアライズ版モジュールの使用をおすすめします。なぜCDRシリアライズ版の方がJSONシリアライズ版よりもデータ処理が軽くなるのか技術的な背景は、最下部のNoteにまとめていますので、そちらを参考にしてください。

これに対してJSONシリアライズ版モジュールは、データポート間の通信パフォーマンスはCDRシリアライズ版モジュールに劣後するものの、**RTシステム外部のMQTTシステムやAWS等が提供するクラウドサービスとの連携が可能**になる等、拡張性が増します。すなわちJSONシリアライズ版モジュールを用いることで、**RTシステムの枠を超えたシステム構築が可能**となります。試しにJSONシリアライズ版モジュールを用いてRTコンポーネントのOutPortからPublishしたデータを、MQTTクライアントライブラリを用いて構築した通常のMQTTクライアントでSubscribeしてみると、JSON形式でシリアライズされたTextデータを取得できることがわかります。これとは逆にJSON形式でシリアライズされたデータを通常のMQTTクライアントからPublishし、RTコンポーネントのInPortでSubscribeすることもできます。以上から、JSONシリアライズ版モジュールは、外部システムとの連携が必要等、RTシステム内でMQTT通信が収まらないケースでの使用が適していると言えます。

CDRシリアライズ版とJSONシリアライズ版いずれの通信モジュールもVersion3.1.1のMQTTプロトコルを採用しており、セキュア通信機能のないものとセキュア通信機能付きのものを備えています。モジュール名の接尾辞に'Secure'と表記されているものがセキュア通信対応となります。すなわち、(1),(2),(5)または(6)のモジュールはセキュア通信機能がなく平文での通信となるため、ローカルマシン内やローカルネットワーク内での通信用に限定されます。インターネット等不特定多数の方が利用するネットワーク上にシステムを構築する場合は、セキュア通信機能付きの(3),(4),(7)または(8)のモジュールを使用してください。  

各通信モジュールのプロパティとそのdefault値は以下のとおりです。

**(1) OutPortPahoPublisher, (2) InPortPahoSubscriber, (5) OutPortPahoPubJson** および **(6) InPortPahoSubJson**
||Name (Key)|Default value| 説明 |
| :-- | :-- | :-- | :-- |
| 1. | host | 'localhost' | エンドポイントとなるBrokerのアドレス（FQDNまたはIPアドレス） |
| 2. | msport | 1883 | MQTTメッセージングサービスのポート番号 |
| 3. | kpalv | 60 | Keep alive。コネクション維持のための指標。単位はsで、設定時間内に通信が確認できなければ自動的にコネクションが破棄される |
| 4. | topic | 'test' | メッセージンググループ名。メッセージの送受信を行うクライアントは同一のTopicに属していなければいけない |
| 5. | qos | 0 | メッセージング品質。MQTTでは0, 1, 2の何れかから選択する。数字が大きいほど高品質だが処理的に重くなる |
| 6. | id | None | クライアントID。Brokerに対してuniqueな値でなければいけない。defaultでは乱数により値が与えられる |
| 7. | cs | True | Clean Session。クライアントの接続が切れた場合に、Brokerで接続時のSession情報を残しておくか否か。FalseかつQoS>0の場合、クライアント側ネットワーク障害発生時にBroker側でサブスクリプションおよびメッセージが保存され、Subscriber（InPort）が永続化する |
| 8. | maxif | 20 | Max inflight messages。サーバのACKを待たずに同時発信可能なメッセージの数。値が高ければメッセージングのスループットは向上するが、その分メモリ消費量が大きくなる。OutPortPahoPublisherモジュールまたはOutPortPahoPubJsonモジュールでQoS>0の場合のみ有効 |
| 9. | retain | False | MQTT ver.3.1.1におけるRetain（保持）の機能を使用するか否か。Retainを有効化（True）すると、BrokerにPublisher（OutPort）から送信された最新のメッセージが保持されるようになる。これにより、遅れて参加してきたSubscriber（InPort）は通信頻度が低いシステムにおいても、Brokerに接続後すぐに最新のメッセージを取得することができる。RetainはOutPortPahoPublisherモジュールまたはOutPortPahoPubJsonモジュールでのみ設定可能 |
| 10. | clrrm | False | Clear retained message。RetainによりBrokerに保持された最新メッセージは、明示的に削除されない限り保持が継続する。True指定でBrokerに保持された最新メッセージを削除する。Retainedメッセージの削除は、OutPortPahoPublisherモジュールまたはOutPortPahoPubJsonモジュールからのみ可能 |
| 11. | will | False | MQTT ver.3.1.1におけるWill（遺言）の機能を使用するか否か。Willを有効化（True）すると、Publisher（OutPort）側で何らかの障害が発生し、正常にdisconnectせずにBrokerから切断された場合に、BrokerからSubscriber（InPort）に対して予め指定していたWillメッセージが即座に送信される。WillメッセージはRTMにおける各種データ型の各項目に数値0（文字列の場合は文字0、Booleanの場合はFalse）が入力されたものとなる。現時点では基本データ型（BasicDataTypes）と拡張データ型（ExtendedDataTypes）のみに対応。WillはOutPortPahoPublisherモジュールまたはOutPortPahoPubJsonモジュールでのみ設定可能。*※ rtc.confでpreconnect指定により事前にWillを設定する場合はデータ型の指定も必要。詳細は下記Noteを参照のこと* |

**(3) OutPortPahoPubSecure, (4) InPortPahoSubSecure, (7) OutPortPahoPubJsonSecure** および **(8) InPortPahoSubJsonSecure**
||Name (Key)|Default value| 説明 |
| :-- | :-- | :-- | :-- |
| 1. | host | 'localhost' | エンドポイントとなるBrokerのアドレス（FQDNまたはIPアドレス） |
| 2. | msport | 8883 | MQTTS（MQTT Secure）メッセージングサービスのポート番号 |
| 3. | kpalv | 60 | Keep alive。コネクション維持のための指標。単位はsで、設定時間内に通信が確認できなければ自動的にコネクションが破棄される |
| 4. | topic | 'test' | メッセージンググループ名。メッセージの送受信を行うクライアントは同一のTopicに属していなければいけない |
| 5. | qos | 0 | メッセージング品質。MQTTでは0, 1, 2の何れかから選択する。数字が大きいほど高品質だが処理的に重くなる |
| 6. | id | None | クライアントID。Brokerに対してuniqueな値でなければいけない。defaultでは乱数により値が与えられる |
| 7. | cs | True | Clean Session。クライアントの接続が切れた場合に、Brokerで接続時のSession情報を残しておくか否か。FalseかつQoS>0の場合、クライアント側ネットワーク障害発生時にBroker側でサブスクリプションおよびメッセージが保存され、Subscriberが永続化する |
| 8. | cacert | './ca.crt' | 認証局（Certificate Authority）証明書へのpath。絶対パスと相対パスいずれでも指定可能。サーバの真正性を証明するのに必要 |
| 9. | cltcert | './client.crt' | クライアント証明書へのpath。絶対パスと相対パスいずれでも指定可能。クライアントの真正性を証明するのに必要 |
| 10. | cltkey | './client.key' | クライアント秘密鍵へのpath。絶対パスと相対パスいずれでも指定可能。クライアントの真正性を証明するのに必要 |
| 11. | maxif | 20 | Max inflight messages。サーバのACKを待たずに同時発信可能なメッセージの数。値が高ければメッセージングのスループットは向上するが、その分メモリ消費量が大きくなる。OutPortPahoPubSecureモジュールまたはOutPortPahoPubJsonSecureモジュールでQoS>0の場合のみ有効 |
| 12. | retain | False | MQTT ver.3.1.1におけるRetain（保持）の機能を使用するか否か。Retainを有効化（True）すると、BrokerにPublisher（OutPort）から送信された最新のメッセージが保持されるようになる。これにより、遅れて参加してきたSubscriber（InPort）は通信頻度が低いシステムにおいても、Brokerに接続後すぐに最新のメッセージを取得することができる。RetainはOutPortPahoPubSecureモジュールまたはOutPortPahoPubJsonSecureモジュールでのみ設定可能 |
| 13. | clrrm | False | Clear retained message。RetainによりBrokerに保持された最新メッセージは、明示的に削除されない限り保持が継続する。True指定でBrokerに保持された最新メッセージを削除する。Retainedメッセージの削除は、OutPortPahoPubSecureモジュールまたはOutPortPahoPubJsonSecureモジュールからのみ可能 |
| 14. | will | False | MQTT ver.3.1.1におけるWill（遺言）の機能を使用するか否か。Willを有効化（True）すると、Publisher（OutPort）側で何らかの障害が発生し、正常にdisconnectせずにBrokerから切断された場合に、BrokerからSubscriber（InPort）に対して予め指定していたWillメッセージが即座に送信される。WillメッセージはRTMにおける各種データ型の各項目に数値0（文字列の場合は文字0、Booleanの場合はFalse）が入力されたものとなる。現時点では基本データ型（BasicDataTypes）と拡張データ型（ExtendedDataTypes）のみに対応。WillはOutPortPahoPubSecureモジュールまたはOutPortPahoPubJsonSecureモジュールでのみ設定可能。*※ rtc.confでpreconnect指定により事前にWillを設定する場合はデータ型の指定も必要。詳細は下記Noteを参照のこと* |

プロパティはOpenRTM-aist ver.1.2.0以降であれば、RTコンポーネントの実行前に、rtc.confにて事前設定可能です。このrtc.confを"-f"でオプション指定し、RTコンポーネントを実行することでMQTT Brokerへの接続が完了した状態へと遷移します。なお、Keyは必ずしも上記の順番で入力する必要はありません。いくつかのKeyを選択し、順不同で入力することができます。
```bash
# rtc.conf
：
# MQTT BrokerへのOutPortの自動接続
manager.components.preconnect: ConsoleIn0.out?interface_type=mqtt_cdr&host=127.0.0.1&topic=hoge
```

プロパティの事前設定を利用しない場合、もしくはver.1.2.0より前のバージョンのOpenRTM-aistを利用されている場合は、プロパティは以下のようににロボットシステムの構築ツールであるRTSystemEditor上で、RTコンポーネントにおけるデータポートの接続を行う際に表示されるConnector Profileダイアログの"詳細"からKey-Value形式で直接入力することになります。いくつかのKeyを選択し、順不同で入力可能なのはrtc.confにおける事前設定と同様です。

<img src="https://user-images.githubusercontent.com/40682353/99870217-b3a78380-2c14-11eb-9861-67fc2e78c26b.png" width=50%>

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

(4) githubのリポジトリからMQTT通信モジュールに関連するファイル群をcloneし、MQTT通信モジュール群をインストール。インストール先は`pip3 show OpenRTM_aist_paho_mqtt_module`の"Location"で確認できます。なお、アンインストールする場合は`sudo pip3 uninstall OpenRTM_aist_paho_mqtt_module`で行ってください。
```bash
$ cd ~/
$ git clone https://github.com/dyubicuoa/OpenRTM_aist_paho_mqtt_interface
$ cd OpenRTM_aist_paho_mqtt_interface/OpenRTM_aist_v122l_paho_mqtt_interface
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

(4) githubのリポジトリからMQTT通信モジュールに関連するファイル群をcloneし、MQTT通信モジュール群をインストール。インストール先は`pip show OpenRTM_aist_paho_mqtt_module`の"Location"で確認できます。なお、アンインストールする場合は`sudo pip uninstall OpenRTM_aist_paho_mqtt_module`で行ってください。
```bash
$ cd ~/
$ git clone https://github.com/dyubicuoa/OpenRTM_aist_paho_mqtt_interface
$ cd OpenRTM_aist_paho_mqtt_interface/OpenRTM_aist_v121e_paho_mqtt_interface
$ sudo pip install .
```

## Usage

以下では、Linux（Ubuntu or Debian）の環境下において、OpenRTM-aist上のMQTT通信インタフェースを利用してロボットシステムを構築する手順を2通り示します。一つめは『**MQTT通信モジュールに関連するプロパティをrtc.confで事前に設定し、RTコンポーネント実行時にデータポートをMQTT Brokerに自動接続する方法**』です。もう一つは『**RTコンポーネント実行後にRTSystemEditorを用い、モジュールのプロパティを直接入力し、マニュアルでBrokerに接続する方法**』となります。前者はOpenRTM-aist ver.1.2.0以降で追加された新機能用いるため、ver.1.2.0以降のユーザ用、後者はver.1.2.0より前のバージョンのOpenRTM-aistユーザ、もしくはRTSystemEditor上でマニュアル操作によりロボットシステムを一から構築したいユーザ用です。操作上は、前者がrtc.confからモジュールに対してプロパティを渡せることから、ロボットシステムの構築作業が格段に簡易化されます。ですので、通常は前者の構築手順を選択することになります。  

なお、構築例で使用するのはOpenRTM-aistで予めexampleとして用意されているConsoleInとConsoleOutの各コンポーネントですが、当然ながらエンドユーザが独自に開発したRTコンポーネントにも応用可能です。

#### (0) MQTT Brokerの稼働状況確認
MQTT通信インタフェースの場合、**データポートの接続先はMQTT Broker**となります。CORBAのようにデータポート間で接続されるわけではありません。MQTT通信インタフェースでは各データポートは単独でBrokerに接続する形をとります。このことからロボットシステム構築以前にBrokerが稼働していることが前提条件となります。ですのでRTコンポーネント実行前にまずBrokerが稼働中であることを確認してください。  

Brokerはその運用形態により以下の3種類に分かれます。

1. クラウドサービスとして展開されたIoTプラットフォーム（例：AWS IoT Core, Azure IoT Hub, Google Cloud IoT Core)
1. オンプレミスによる自社運用サーバ
1. エンドユーザ自らが用意したサーバ

１．は24時間運用が基本なのでまず稼働していないということはないでしょう。２．は各社の運用方針に依るところですので、もし停止中であったり動作に問題があるようであればサーバ管理者に問い合わせてください。３．はテスト用やローカルシステム構築のためにエンドユーザ自らが導入したサーバとなります。Brokerソフトウェア導入直後は稼働していない場合が多いので、RTコンポーネント実行前に必ず稼働状況を確認してください。

以下はMosquittoの稼働状況から、inactiveであることを確認した上でBrokerによるメッセージングサービスをバックグラウンドプロセスとしてスタートさせる例です。
```bash
$ sudo systemctl status mosquitto.service
● mosquitto.service - Mosquitto MQTT Broker
   Loaded: loaded (/lib/systemd/system/mosquitto.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
     Docs: man:mosquitto.conf(5)
           man:mosquitto(8)
：
$ sudo systemctl start mosquitto.service
$ sudo systemctl status mosquitto.service
● mosquitto.service - Mosquitto MQTT Broker
   Loaded: loaded (/lib/systemd/system/mosquitto.service; disabled; vendor preset: enabled)
   Active: active (running) since 月 2020-09-21 10:53:24 JST; 1min 37s ago
     Docs: man:mosquitto.conf(5)
           man:mosquitto(8)
  Process: 18424 ExecStartPre=/bin/chown mosquitto: /var/log/mosquitto (code=exited, status=0/SUCCESS)
  Process: 18420 ExecStartPre=/bin/mkdir -m 740 -p /var/log/mosquitto (code=exited, status=0/SUCCESS)
 Main PID: 18427 (mosquitto)
    Tasks: 1
   Memory: 1.4M
      CPU: 69ms
   CGroup: /system.slice/mosquitto.service
           └─18427 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
：
```

### 『プロパティの事前設定とMQTT Brokerへの自動接続によりRTシステムを構築する手順』

#### (1) rtc.confでのモジュール指定とプロパティ設定
MQTT通信モジュールをOpenRTM-aistに動的に組み込むには、MQTTで通信を行いたいRTコンポーネントのrtc.confにおいて、"**manager.modules.load_path:**"にてMQTT通信モジュールへのpathを、"**manager.modules.preload:**"にてモジュール名を指定する必要があります。OutPortはデータを送信する側なので、(1) OutPortPahoPublisher, (3) OutPortPahoPubSecure, (5) OutPortPahoPubJsonもしくは(7) OutPortPahoPubJsonSecureのいずれかのMQTT Publisher通信モジュールを指定します。一方、InPortはデータを受信する側なので、(2) InPortPahoSubscriber, (4) InPortPahoSubSecure, (6) InPortPahoSubJsonもしくは(8) InPortPahoSubJsonSecureのいずれかのMQTT Subscriber通信モジュールを指定します。

続いて、プロパティの設定です。モジュールのプロパティをrtc.confで事前に設定し、RTコンポーネントの実行と同時に対象のデータポートをMQTT Brokerに自動的に接続するには"**manager.components.preconnect:**"指定を利用します。preconnectによるMQTT通信インタフェースや関連するプロパティ等の設定方法は以下の通りです。
```bash
manager.components.preconnect: \
{RTコンポーネント名}.{データポート名}?interface_type={MQTT通信インタフェース名}&{プロパティのkey}={プロパティのvalue}&...
```

さらに"**manager.components.preactivation:**"指定を用いることで対象のRTコンポーネントの自動Activate化が可能となります。preactivationによるRTコンポーネントの指定方法は以下の通りです。
```bash
manager.components.preactivation: {RTコンポーネント名}
```

例えば、RTコンポーネントConsoleInにおけるOutPort名"out"でInterface Typeとしてセキュア通信機能なしのCDRシリアライズ版MQTT通信インタフェースを選択した上で、BrokerエンドポイントアドレスとTopic名の各プロパティを設定し、Brokerへの自動接続を行いたい場合は、以下のようにrtc.confに追記します。
```bash
# rtcPrePub.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python3.6/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPublisher.py
# MQTT BrokerへのOutPortの自動接続
manager.components.preconnect: ConsoleIn0.out?interface_type=mqtt_cdr&host=127.0.0.1&topic=hoge
```

RTコンポーネントConsoleOutにおけるInPort名"in"でInterface Typeとしてセキュア通信機能なしのCDRシリアライズ版MQTT通信インタフェースを選択した上で、QoSとTopicの各プロパティを設定し、Brokerへの自動接続とRTコンポーネントの自動Activate化を行いたい場合は以下の通り。
```bash
# rtcPreSub.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python3.6/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: InPortPahoSubscriber.py
# RTコンポーネントの自動Activate化
manager.components.preactivation: ConsoleOut0
# MQTT BrokerへのInPortの自動接続
manager.components.preconnect: ConsoleOut0.in?interface_type=mqtt_cdr&qos=1&topic=hoge
```

RTコンポーネントConsoleInにおけるOutPort名"out"でInterface Typeとしてセキュア通信機能なしのJSONシリアライズ版MQTT通信インタフェースを選択した上で、Retain（保持）とWill（遺言）の機能を2つとも使用したい場合は以下の通り。なお、TrueやFalseの指定は大文字でも小文字でも頭文字だけ（'t','T','f'または'F'）でも通ります。
```bash
# rtcPrePubJson.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python3.6/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPubJson.py
# MQTT BrokerへのOutPortの自動接続
manager.components.preconnect: ConsoleIn0.out?interface_type=mqtt_json&data_type=TimedLong&retain=true&will=true
```

注意点ですが、**preconnect指定によりJSONシリアライズ版MQTT通信モジュールを利用する場合はデータポートのデータ型を"data_type"にて指定する必要があります**。RTSystemEditorで直接プロパティを入力する場合はデータ型を指定する必要はありません。また、CDRシリアライズ版かJSONシリアライズ版に関係なくMQTTの一部機能である'Will'を利用する場合も、これと同様にpreconnect指定で事前設定するケースにおいてのみデータ型の指定が必要です。詳細は最下部のNote『OutPortPahoPublisherまたはOutPortPahoPubSecureモジュールのrtc.confでpreconnect指定により事前にWillを設定するには』を参照してください。

一つのRTコンポーネント（RTC名：PahoMqttTest）にOutPort(ポート名：out）もInPort（ポート名：in）も備わっており、そのどちらもセキュア通信機能付きのCDRシリアライズ版MQTT通信インタフェースを通してデータの送受信を行いたい場合は以下のように","で区切ってモジュール名を2つ指定します。どちらのデータポートもBrokerへの自動接続を行いたい場合も同様に","で区切って、各データポートの通信インタフェースや関連するプロパティを設定します。
```bash
# rtcPrePubSubSecure.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python3.6/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPubSecure.py, InPortPahoSubSecure.py
# MQTT Brokerへの2つのデータポート（OutPortとInPort）の自動接続
manager.components.preconnect: \
PahoMqttTest0.out?interface_type=mqtts_cdr&cacert=./tls/ca.crt&cltcert=./tls/clt.crt&cltkey=./tls/clt.key, \
PahoMqttTest0.in?interface_type=mqtts_cdr&cacert=./tls/ca.crt&cltcert=./tls/clt.crt&cltkey=./tls/clt.key
```

MQTT通信モジュールへのpathはインストール先を指定するか、インストール後であればcloneしたレポジトリ内にあるモジュールを指定しても構いません。"rtc.conf"の設定例はリポジトリの"OpenRTM_aist_paho_mqtt_module/samples/rtc_conf/"配下に置いてあるので参考にしてください。


#### (2) RTコンポーネントの実行
(1)で設定したrtc.confを"-f"オプションで指定し、ターゲットとなるRTコンポーネントを実行します。

以下はConsoleInとConsoleOutの各コンポーネントの実行例です。ConsoleInはOutPortを備えているのでrtcPrePub.confを、ConsoleOutはInPortを備えているのでrtcPreSub.confをそれぞれオプションとして指定します。
```bash
$ python3 ConsoleIn.py -f rtcPrePub.conf
PahoPublisher constructor was called.
Server address: 127.0.0.1
Port number not found. Default port '1883' is used.
Keepalive not found. Default keepalve '60' is used.
Topic: hoge
QoS not found. Default QoS '0' is used.
Client ID not found. Random number ID is used.
CleanSession not found. Default clean_session 'True' is used.
MaxInflight not found. Default max_inflight '20' is used.
Retained not found. Default retained 'False' is used.
Last will not found. Default last will 'False' is used.
[connecting to MQTT broker start]
 connected to broker.
[connecting to MQTT broker end]
:
```
```bash
$ python3 ConsoleOut.py -f rtcPreSub.conf
PahoSubscriber constructor was called.
Server address not found. Default server address 'localhost' is used.
Port number not found. Default port '1883' is used.
Keepalive not found. Default keepalve '60' is used.
Topic: hoge
QoS: 1
Client ID not found. Random number ID is used.
CleanSession not found. Default clean_session 'True' is used.
[connecting to MQTT broker start]
 connected to broker.
[connecting to MQTT broker end]
Subscription started: 1 (0,)
:
```

このようにrtc.confで指定したpreconnet機能により、MQTT Brokerに接続された状態で各コンポーネントが起動します。Brokerへの接続が成功すると上記のように接続時の各種プロパティ情報とともに"connected to broker."と表示されます。加えてSubscriber側であるInPortではデータの受信を開始すると"Subscription started:"も同時に表示されます。

この状態、すなわちConsoleInがBrokerへの接続が完了した状態、ConsoleOutがこれに加えてActivate化まで完了した状態でRTSystemEditorで各コンポーネントを表示すると以下のようになります。

<img src="https://user-images.githubusercontent.com/40682353/93737397-10d78680-fc1e-11ea-8987-4da792f94b0e.png" width=70%>

BrokerはRTSystemEditor上では表示されません。しかし、OutPortとInPortの各データポートが緑色になっていれば、Brokerへの接続が完了していることを示しています。後は通常通り、RTSystemEditorでConsoleInをActivate化すればRTシステムが稼働します。Deactivate化も同様にRTSystemEditorから実行可能です。

### 『RTSystemEditor上でのマニュアル操作によりRTシステムを構築する手順』

#### (1) rtc.confでのモジュール指定
MQTT通信モジュールをOpenRTM-aistに動的に組み込むには、MQTTで通信を行いたいRTコンポーネントのrtc.confにおいて、"**manager.modules.load_path:**"にてMQTT通信モジュールへのpathを、"**manager.modules.preload:**"にてモジュール名を指定する必要があります。OutPortはデータを送信する側なので、(1) OutPortPahoPublisher, (3) OutPortPahoPubSecure, (5) OutPortPahoPubJsonもしくは(7) OutPortPahoPubJsonSecureのいずれかのMQTT Publisher通信モジュールを指定します。一方、InPortはデータを受信する側なので、(2) InPortPahoSubscriber, (4) InPortPahoSubSecure, (6) InPortPahoSubJsonもしくは(8) InPortPahoSubJsonSecureのいずれかのMQTT Subscriber通信モジュールを指定します。

例えば、セキュア通信機能なしのCDRシリアライズ版MQTT通信インタフェースを用いてOutPortからデータを送信したい場合は以下のようにrtc.confに記述します。
```bash
# rtcPub.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPublisher.py
```

セキュア通信機能なしのCDRシリアライズ版MQTT通信インタフェースを用いてInPortにてデータを受信したい場合は以下の通り。
```bash
# rtcSub.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: InPortPahoSubscriber.py
```

セキュア通信機能なしのJSONシリアライズ版MQTT通信インタフェースを用いてInPortにてデータを受信したい場合は以下の通り。
```bash
# rtcSubJson.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: InPortPahoSubJson.py
```

一つのRTコンポーネントにOutPortもInPortも備わっており、そのどちらもセキュア通信機能付きのCDRシリアライズ版MQTT通信インタフェースを通してデータの送受信を行いたい場合は以下のように","で区切ってモジュール名を2つ指定します。
```bash
# rtcPubSubSecure.conf
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python2.7/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPubSecure.py, InPortPahoSubSecure.py
```

MQTT通信モジュールへのpathはインストール先を指定するか、インストール後であればcloneしたレポジトリ内にあるモジュールを指定しても構いません。"rtc.conf"の設定例はリポジトリの"OpenRTM_aist_paho_mqtt_module/samples/rtc_conf/"配下に置いてあるので参考にしてください。

#### (2) RTコンポーネントの実行
(1)で設定したrtc.confをオプションで指定し、ターゲットとなるRTコンポーネントを実行します。

以下はConsoleInとConsoleOutの各コンポーネントの実行例です。ConsoleInはOutPortを備えているのでrtcPub.confを、ConsoleOutはInPortを備えているのでrtcSub.confをそれぞれオプションとして指定します。
```bash
$ python ConsoleIn.py -f rtcPub.conf
```
```bash
$ python ConsoleOut.py -f rtcSub.conf
```

#### (3) データポートとBrokerの接続
<img src="https://user-images.githubusercontent.com/40682353/93169247-aa56f200-f75f-11ea-9cf0-c38fff156859.png" width=70%>

OpenRTPを起動し、RTSystemEditorのSystem Diagramに先ほど実行したRTコンポーネントをセットします。

<img src="https://user-images.githubusercontent.com/40682353/93169326-d4a8af80-f75f-11ea-845a-9a0dc91d97df.png" width=70%>

データ送信側RTコンポーネントConsoleInのOutPortを右クリックし、"接続"を選択します。

<img src="https://user-images.githubusercontent.com/40682353/99870241-05e8a480-2c15-11eb-982c-0aa3d80ac242.png" width=40%>

Connector Profileダイアログが立ち上がるのでProfile中の【Interface Type】から"mqtt_cdr"を選択します。これで通信インタフェースがCORBAからMQTTへと切り替わります。なお、【Interface Type】はセキュア通信機能付きCDRシリアライズ版モジュールの場合は"mqtts_cdr"、セキュア通信機能なしJSONシリアライズ版モジュールの場合は"mqtt_json"、セキュア通信機能付きJSONシリアライズ版モジュールの場合は"mqtts_json"と表記されることになります。

<img src="https://user-images.githubusercontent.com/40682353/99870296-67107800-2c15-11eb-8b77-9f991c7fdd9a.png" width=40%>

MQTT通信モジュールのプロパティをdefaultのまま使用する場合は右下の"OK"ボタンをクリックすることでdefaultの情報でMQTT Brokerへの接続が行われます。OutPortが緑色になればBrokerへの接続完了です。MQTT通信モジュールのプロパティを変更したい場合は、モジュールに渡すプロパティを設定するため、左下の"詳細"をチェックします。

<img src="https://user-images.githubusercontent.com/40682353/99870313-84454680-2c15-11eb-9e74-655a181f1158.png" width=50%>

Connector ProfileダイアログにBufferの各種設定と、MQTT通信モジュールのプロパティ設定を行えるダイアログが追加表示されます。最下部の"Name"および"Value"と表示されている部分がプロパティ設定箇所です。右横の"追加"ボタンをクリックします。

<img src="https://user-images.githubusercontent.com/40682353/99870322-9e7f2480-2c15-11eb-9d9d-463000433400.png" width=50%>

プロパティの設定箇所が追加されます。複数のプロパティを変更する場合は必要分"追加"ボタンをクリックしてください。プロパティはNameとValueの組み合わせ、すなわちkey-value型で設定できます。Featuresで示した設定可能なプロパティを参照しながら、変更が必要なプロパティを入力します。例えばMQTT BrokerのアドレスとTopic名を変更したい場合は次のように入力します。なお、Brokerの設定次第では使用可能なTopicが制限されていることもあるのでサーバの管理者に、クライアント側でTopicを設定可能かどうか予め確認しておきましょう。

<img src="https://user-images.githubusercontent.com/40682353/99870341-b9ea2f80-2c15-11eb-8b59-e8387d27d0cc.png" width=50%>

プロパティ設定後、右下の"OK"ボタンをクリックすれば、入力したプロパティがMQTT通信モジュールに反映され、更新された情報を元にMQTT Brokerへの接続が行われます。

<img src="https://user-images.githubusercontent.com/40682353/93169472-20f3ef80-f760-11ea-88af-32beee2dcf1e.png" width=70%>

このように、MQTT通信インタフェースを用いた場合はデータポート単体でBrokerに接続する形をとります。このため、データポート間での結線は行いません。なぜならばMQTTにおけるPublisher（送信者）とSubscriber（受信者）の各クライアントの接続先はサーバとなるBrokerであり、お互いに直接的に接続する通信アーキテクチャとはなっていないためです。BrokerはRTSystemEditor上では表示されませんが、データポートが緑色に変わればBrokerへの接続は成功しています。

<img src="https://user-images.githubusercontent.com/40682353/93169504-2d784800-f760-11ea-9b64-49ad91b6675c.png" width=70%>

データ受信側RTコンポーネントConsoleOutも同じ要領で、InPort右クリックからConnector Profileの設定を行い、MQTT Brokerに単体で接続します。その後、通常通りそれぞれのRTコンポーネントをAvtivate化することでRTシステムが稼働します。

## Note

### データポート間の結線について
RTSystemEditorからの直接操作により、MQTT通信インタフェースを通してデータポートをMQTT Brokerへ接続する際は、**データポート右クリックでの接続が基本**となります。データポート間の結線によるBrokerへの接続も可能ですが、できるだけ行わないでください。どうしても結線したい場合はプロパティのClient IDはバッティングを避けるため、デフォルトのランダム値を使用するようにしてください。また、1対Nで結線する場合、例えばOutPort一つに対して複数のInPortをすべて結線してBrokerに接続するケースにおいては、OutPort側の通信モジュールのインスタンスが複数立ち上がるため、同一Topicのままだとメッセージングが多重化してしまい想定通りの通信を行えなくなるので気をつけてください。このケースでは、一つの結線ごとに別のTopicを設定することで問題を回避できます。

### MQTT通信インタフェース動作確認用 Example RTC の起動スクリプト
産業技術総合研究所 安藤様から、OpenRTM-aistで用意されているRTコンポーネントのExampleのうち、"SeqIO"と"SimpleIO"、"Slider_and_Motor"の起動スクリプトをご提供いただきました。MQTT通信インタフェースの動作確認を手早く行いたい方向けのスクリプトとなります。samples/launch_scriptsフォルダ内に追加しましたのでよろしければお試しください。

なお、起動スクリプトの実行には、実行するローカルマシン内で稼働する何らかのMQTT Brokerが必要となります。起動スクリプトの実行前に、Eclipse Mosquitto等OSSのBrokerを予めインストールし起動しておいてください。

また、"Slider_and_Motor"についてはパッケージ"python3-tk"（Python3系）もしくは"python-tk"（Python2系）が必要になります。script実行前に、コマンドラインから`sudo apt install python3-tk`または`sudo apt install python-tk`により、該当のパッケージをインストールしてください。これに加えて、"Slider_and_Motor"の実行可能な環境はDesktopのみとなります。Server環境やDocker等のContainer環境を使用されている方はご注意ください。

### AWS IoT Core への接続について
セキュア通信機能付きMQTT通信モジュール（OutPortPahoPubSecureまたはInPortPahoSubSecure）を用いれば、IoTプラットフォームの AWS IoT Core を中継地点（Broker）としたデータポート間のデータ送受信が可能です。AWSにてThing設定時に得られた情報をもとに、IoT Core へ接続したいRTコンポーネントのrtc.confを以下のように書き換えてください。以下の事例はOutPortを Iot Core に接続するケースとなります。
```bash
# rtc.conf example to connect to AWS IoT Core
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python3.6/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPubSecure.py
# AWS IoT CoreへのOutPortの自動接続
manager.components.preconnect: \
PahoMqttTest0.out?interface_type=paho_mqtts&host={AWSから割り当てられたエンドポイント}&cacert={AWSで発行されたルート認証局証明書へのpath}&cltcert={AWSで発行されたクライアント証明書へのpath}&cltkey={AWSで発行されたクライアント秘密鍵へのpath}
```

なお、AWS IoT Core では、Topicは利用者側で自由に設定できますが、QoSは0または1のみが有効です。QoS=2は選択できませんのでご注意ください。

また、CDRシリアライズ版MQTT通信モジュールは、IoT Coreを介したデータポート間のPublish/Subscribeのみに対応しています。AWS側とはメッセージ中のpayloadのデータ形式やシリアライズ形式が異なるため、Amazon LambdaやAmazon Kinesis等他のAWSクラウドサービスとの連携はできません。RTコンポーネントとAWSで提供している他のクラウドサービスとの連携を図りたい場合は、JSONシリアライズ版MQTT通信モジュールを使用してください。

### OutPortPahoPublisherまたはOutPortPahoPubSecureモジュールのrtc.confでpreconnect指定により事前にWillを設定するには
以下のように、rtc.conf内でpreconnect指定により、willの設定に加えて、データポートのデータ型（data_type）も設定する必要があります。
```bash
# rtc.conf example to enable 'Will' function
：
# MQTT通信モジュールへのpath
manager.modules.load_path: /usr/local/lib/python3.6/dist-packages/OpenRTM_aist_paho_mqtt_module
# MQTT通信モジュール名
manager.modules.preload: OutPortPahoPublisher.py
# Willの有効化
manager.components.preconnect: \
ConsoleIn0.out?interface_type=paho_mqtt&will=True&data_type=TimedLong
```

これに対して、RTSystemEditorにて直接プロパティを設定するケースにおいては、データ型を入力する必要はありません。Name-Valueの設定箇所でwillをTrueに設定するだけで足ります。

これは、OpenRTM-aistにおける各種データ型に対応したWillメッセージを作成する上で、ミドルウェア側からデータポートのデータ型を取得する必要があるのですが、rtc.confのpreconnect指定ではデータ型のプロパティを取得できないためです。RTSystemEditorからの直接操作でWillを設定する場合においては、問題なくミドルウェア側からデータ型を取得できるため、データ型の入力は省略することができます。

### 動作確認済みの環境
* Ubuntu 16.04, x86-64 CPU
* Ubuntu 18.04, x86-64 CPU
* Ubuntu 20.04, x86-64 CPU
* Debian 9 (Stretch), x86-64 CPU
* Raspbian (Stretch), ARM CPU
* Raspberry Pi OS (Buster), ARM CPU
 
## Author

* 吉野 大志 (Daishi Yoshino)
* 会津大学 復興支援センター (Revitalization center, University of Aizu)
* FB: https://www.facebook.com/daishi.y.uoa
 
## License
 
"OpenRTM-aist Python用 Paho MQTT通信モジュール" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
