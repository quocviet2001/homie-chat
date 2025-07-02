<?php
     namespace App\Models;

     use Illuminate\Database\Eloquent\Model;

     class Friend extends Model
     {
         protected $table = 'friends';

         protected $primaryKey = null;

         public $incrementing = false;

         protected $fillable = [
             'user_id',
             'friend_id',
         ];

         public $timestamps = true;

         public function user()
         {
             return $this->belongsTo(User::class, 'user_id');
         }

         public function friend()
         {
             return $this->belongsTo(User::class, 'friend_id');
         }
     }
