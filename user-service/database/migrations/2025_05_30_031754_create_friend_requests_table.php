<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFriendRequestsTable extends Migration
     {
         public function up()
         {
             Schema::create('friend_requests', function (Blueprint $table) {
                 $table->bigIncrements('id');
                 $table->bigInteger('sender_id')->unsigned();
                 $table->bigInteger('receiver_id')->unsigned();
                 $table->enum('status', ['pending', 'accepted', 'rejected'])->default('pending');
                 $table->timestamps();
                 $table->foreign('sender_id')->references('id')->on('users')->onDelete('cascade');
                 $table->foreign('receiver_id')->references('id')->on('users')->onDelete('cascade');
                 $table->unique(['sender_id', 'receiver_id']);
             });
         }

         public function down()
         {
             Schema::dropIfExists('friend_requests');
         }
     }
