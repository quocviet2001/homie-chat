<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFriendsTable extends Migration
     {
         public function up()
         {
             Schema::create('friends', function (Blueprint $table) {
                 $table->bigInteger('user_id')->unsigned();
                 $table->bigInteger('friend_id')->unsigned();
                 $table->timestamp('created_at')->useCurrent();
                 $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
                 $table->foreign('friend_id')->references('id')->on('users')->onDelete('cascade');
                 $table->primary(['user_id', 'friend_id']);
             });
         }

         public function down()
         {
             Schema::dropIfExists('friends');
         }
     }
