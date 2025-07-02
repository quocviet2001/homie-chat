<?php

     use Illuminate\Database\Migrations\Migration;
     use Illuminate\Database\Schema\Blueprint;
     use Illuminate\Support\Facades\Schema;

     class AddTimestampsToFriendsTable extends Migration
     {
         public function up(): void
         {
             Schema::table('friends', function (Blueprint $table) {
                 if (!Schema::hasColumn('friends', 'created_at')) {
                     $table->timestamp('created_at')->nullable();
                 }
                 if (!Schema::hasColumn('friends', 'updated_at')) {
                     $table->timestamp('updated_at')->nullable();
                 }
             });
         }

         public function down(): void
         {
             Schema::table('friends', function (Blueprint $table) {
                 if (Schema::hasColumn('friends', 'created_at')) {
                     $table->dropColumn('created_at');
                 }
                 if (Schema::hasColumn('friends', 'updated_at')) {
                     $table->dropColumn('updated_at');
                 }
             });
         }
     }