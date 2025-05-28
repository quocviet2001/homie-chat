<?php
// Import Route facade để định nghĩa route
use Illuminate\Support\Facades\Route;

// Route cơ bản để kiểm tra User Service
Route::get('/', function () {
    // Trả về JSON để xác nhận User Service hoạt động
    return response()->json(['message' => 'Homie Chat User Service is running']);
});
