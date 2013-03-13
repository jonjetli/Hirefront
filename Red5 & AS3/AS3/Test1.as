package  {
	import flash.media.Camera;
	import flash.media.Microphone;
	import flash.media.Video;
	import flash.events.NetStatusEvent;
	import flash.display.Sprite;
	import flash.net.NetConnection;
	import flash.net.NetStream;
	import flash.events.StatusEvent;
	
	public class Test1 extends Sprite {
		
		private var netConnection:NetConnection;
		private var rtmpStr:String;
		private var nsSubscribe:NetStream;
		private var nsPublish:NetStream;
		private var camera:Camera;
		private var microphone:Microphone;
		private var user1Video:Video;
		private var user2Video:Video;

	public function Test1 (){
	
	//rtmpStr="rtmp://192.168.1.132/hirefront"; 
	rtmpStr="rtmp://127.0.0.1/hirefront"; 
	attachCamera();
	attachMicrophone();
	attachVideoObjects();
	
	netConnection=new NetConnection();
	netConnection.addEventListener (NetStatusEvent.NET_STATUS,checkForConnection);
	netConnection.connect(rtmpStr);
	
	}
	
	private function checkForConnection(event:NetStatusEvent):void{
	
	event.info.code == "NetConnection.Connect.Success";
	
	if (event.info.code){
	nsPublish=new NetStream(netConnection);
	nsPublish.attachAudio (microphone);
	nsPublish.attachCamera (camera);
	nsPublish.publish("user1","live");
	nsSubscribe=new NetStream(netConnection);
	nsSubscribe.play("user2");
	user2Video.attachNetStream(nsSubscribe);
		}
	}
	
	private function attachCamera(){
	
	camera=Camera.getCamera();
	//camera.addEventListener(StatusEvent.STATUS, cameraStatusEvent);
	camera.setKeyFrameInterval (32);
	camera.setMode (400,400,15);
	camera.setQuality (0,90);
	}
	
	private function attachMicrophone(){
	
	microphone=Microphone.getMicrophone();
	microphone.gain=80;
	microphone.rate=22;
	microphone.setSilenceLevel(15,2000);
	}
	
	private function attachVideoObjects(){
	
	user1Video=new Video(camera.width,camera.height);
	//addChild(user1Video);
	//user1Video.x=25;
	//user1Video.y=35;
	user1Video.attachCamera(camera);
	user2Video=new Video(600,450);
	addChild(user2Video);
	//user2Video.x=(user1Video.x+ camera.width +15);
	user2Video.x=0;
	user2Video.y=-40;
	} 
	
}
}
