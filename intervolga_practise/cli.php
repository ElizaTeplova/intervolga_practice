<?php

require __DIR__ . "/vendor/autoload.php";
include __DIR__ . "/vendor/vlucas/phpdotenv/src/Dotenv.php";

use Dotenv\Dotenv;
use App\Services\LogAPIService;
use App\Config\RequestParams;

$logApi = new LogAPIService();
$dotenv = Dotenv::createImmutable('./');
$dotenv->load();

$url = "https://api-metrika.yandex.net/management/v1/counter/{$_ENV['COUNTER_ID']}/logrequests";
$authorization = "Authorization: Bearer " . $_ENV['TOKEN'];
$params = new RequestParams();

$url = "https://api-metrika.yandex.net/management/v1/counter/{$_ENV['COUNTER_ID']}/logrequests";
$authorization = "Authorization: Bearer " . $_ENV['TOKEN'];
$params = new RequestParams(date1: date('Y-m-d', strtotime('-91 days')));

$logApi->getCsvData($_ENV['COUNTER_ID'], $_ENV['TOKEN'], $params->getParams(), false);
// $logApi->evaluateRequest($counterId, $token, $params->getParams());
// $logApi->createLogs($_ENV['COUNTER_ID'], $_ENV['TOKEN'], $params->getParams());
// $logApi->getPartNumbers($_ENV['COUNTER_ID'], $_ENV['TOKEN'], requestId: '');
// $logApi->downloadParts($_ENV['COUNTER_ID'], $_ENV['TOKEN'], requestId: '33774523', partNums: 2);
