<?php
declare(strict_types=1);

header('X-Content-Type-Options: nosniff');

function json_response(int $status, array $payload): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_response(405, ['ok' => false, 'error' => 'method']);
}

$honeypot = trim((string) ($_POST['website'] ?? ''));
if ($honeypot !== '') {
    json_response(200, ['ok' => true]);
}

$name = trim((string) ($_POST['name'] ?? ''));
$email = trim((string) ($_POST['email'] ?? ''));
$company = trim((string) ($_POST['company'] ?? ''));
$topic = trim((string) ($_POST['topic'] ?? ''));
$message = trim((string) ($_POST['message'] ?? ''));

if ($name === '' || $email === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    json_response(400, ['ok' => false, 'error' => 'validation']);
}

$to = getenv('LEARNBOX_MAIL_TO') ?: 'nicole.straehl@learnbox.ch';
$subject = 'Anfrage über learnbox.ch: ' . ($topic !== '' ? $topic : 'Kontakt');
$body = "Name: {$name}\nE-Mail: {$email}\nFirma: {$company}\nThema: {$topic}\n\n{$message}\n";
$encodedName = mb_encode_mimeheader($name, 'UTF-8');
$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    "From: learnbox Website <noreply@learnbox.ch>",
    "Reply-To: {$encodedName} <{$email}>",
];

$sent = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));

if (!$sent) {
    json_response(500, ['ok' => false, 'error' => 'mail']);
}

json_response(200, ['ok' => true]);
