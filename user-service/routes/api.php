<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\FriendController;

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// Route yêu cầu xác thực JWT
Route::middleware('auth:api')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', [UserController::class, 'show']);
    Route::put('/user', [UserController::class, 'update']);
    Route::get('/friends', [FriendController::class, 'index']);
    Route::get('/friends/search', [FriendController::class, 'search']);
    Route::post('/friend-requests', [FriendController::class, 'sendRequest']);
    Route::get('/friend-requests', [FriendController::class, 'requests']);
    Route::put('/friend-requests', [FriendController::class, 'respondRequest']);
});

// Route kiểm tra service
Route::get('/', function () {
    return response()->json(['message' => 'Homie Chat User Service is running']);
});
