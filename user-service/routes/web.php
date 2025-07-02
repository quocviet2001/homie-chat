<?php

use Illuminate\Support\Facades\Route;

Route::get('/{any}', function () {
    return ['message' => 'Homie Chat User Service Web route (unused)'];
})->where('any', '.*');

