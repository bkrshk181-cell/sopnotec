<?php
// Lead form handler for cctv.sopnotec.com — emails each request to the SopnoTec mailbox.
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed.']);
    exit;
}

// Honeypot: real visitors never fill this hidden field.
if (!empty($_POST['website'])) {
    echo json_encode(['ok' => true]);
    exit;
}

function field($key, $max = 500) {
    $v = isset($_POST[$key]) ? (string) $_POST[$key] : '';
    $v = trim(strip_tags($v));
    if (function_exists('mb_substr')) { $v = mb_substr($v, 0, $max); } else { $v = substr($v, 0, $max); }
    return $v;
}
function oneline($v) { return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v)); }

$name     = oneline(field('name', 120));
$business = oneline(field('business', 160));
$emailRaw = oneline(field('email', 160));
$email    = filter_var($emailRaw, FILTER_VALIDATE_EMAIL);
$phone    = oneline(field('phone', 40));
$siteType = oneline(field('site_type', 60));
$cameras  = oneline(field('cameras', 10));
$message  = field('message', 3000);

if ($name === '' || !$email) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Please add your name and a valid email address.']);
    exit;
}

$to      = 'abubakar@sopnotec.com';
$subject = 'New CCTV monitoring lead: ' . $name . ($business !== '' ? ' (' . $business . ')' : '');
$body    = "New free-assessment request from cctv.sopnotec.com\n\n"
         . "Name: $name\n"
         . "Business: $business\n"
         . "Email: $email\n"
         . "Phone: $phone\n"
         . "Site type: $siteType\n"
         . "Cameras: $cameras\n\n"
         . "Message:\n$message\n\n"
         . "Sent: " . gmdate('Y-m-d H:i') . " UTC\n";
$headers = "From: SopnoTec CCTV Website <abubakar@sopnotec.com>\r\n"
         . "Reply-To: $email\r\n"
         . "MIME-Version: 1.0\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";

$ok = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f abubakar@sopnotec.com');

if (!$ok) { http_response_code(500); }
echo json_encode(['ok' => (bool) $ok, 'error' => $ok ? null : 'We could not send your request. Please email abubakar@sopnotec.com.']);
