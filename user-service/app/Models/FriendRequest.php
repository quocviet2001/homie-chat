<?php
     namespace App\Models;

     use Illuminate\Database\Eloquent\Model;

     class FriendRequest extends Model
     {
         protected $table = 'friend_requests';

         protected $fillable = [
             'sender_id',
             'receiver_id',
             'status',
         ];

         protected $casts = [
             'status' => 'string',
         ];

         public function sender()
         {
             return $this->belongsTo(User::class, 'sender_id');
         }

         public function receiver()
         {
             return $this->belongsTo(User::class, 'receiver_id');
         }
     }
