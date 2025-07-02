<?php
     namespace App\Models;

     use Illuminate\Foundation\Auth\User as Authenticatable;
     use Tymon\JWTAuth\Contracts\JWTSubject;

     class User extends Authenticatable implements JWTSubject
     {
         protected $table = 'users';

         protected $fillable = [
             'name', 'email', 'password', 'phone', 'avatar'
         ];

         protected $hidden = [
             'password', 'remember_token',
         ];

         protected $casts = [
             'email_verified_at' => 'datetime',
         ];

         public function getJWTIdentifier()
         {
             return $this->getKey();
         }

         public function getJWTCustomClaims()
         {
             return [];
         }

         public function friends()
         {
             return $this->belongsToMany(User::class, 'friends', 'user_id', 'friend_id')
                        ->withTimestamps();
         }

         public function sentFriendRequests()
         {
             return $this->hasMany(FriendRequest::class, 'sender_id');
         }

         public function receivedFriendRequests()
         {
             return $this->hasMany(FriendRequest::class, 'receiver_id');
         }
     }