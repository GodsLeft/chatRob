<?php

namespace AppBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Doctrine\ORM\Query;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

//这个跟我没有太大关系
class ChatBotController extends Controller{
	public function indexAction(){
		return $this->render('chatbot/index.html.twig', array(
			'tophotblogs' => BlogController::getTopHtopBlogs($this, 10)));
	}

	public function queryAction(Request $request){
		$q = $request->get('input');
		$opts = array(
			'http'=> array('method'=>"GET", 'timeout'=>60,));
		$context = stream_context_create($opts);
		$clientIp = $request->getClientIp();
		$response = file_get_contents('http://127.0.0.1:8765/?q=' . urlencode($q) . '&clientIp=' . $clientIp, false, $context);
		$res = json_decode($response, true);
		$total = $res['total'];
		$result = '';
		if($total > 0){
			$result = $res['result'][0]['answer'];
		}
		return new Response($result);
	}
}
