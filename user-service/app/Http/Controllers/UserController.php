<?php
     namespace App\Http\Controllers;

     use Illuminate\Http\Request;
     use Illuminate\Support\Facades\Hash;
     use Tymon\JWTAuth\Facades\JWTAuth;

     class UserController extends Controller
     {
         // Lấy thông tin người dùng hiện tại
         public function show()
         {
             $user = JWTAuth::user();
             return response()->json($user);
         }

         // Cập nhật thông tin cá nhân
         public function update(Request $request)
         {
             $validated = $request->validate([
                 'name' => 'string|max:255',
                 'phone' => 'nullable|string|max:20',
                 'avatar' => 'nullable|string|max:255',
                 'password' => 'nullable|string|min:6',
             ]);

             $user = JWTAuth::user();

             if (isset($validated['name'])) {
                 $user->name = $validated['name'];
             }
             if (isset($validated['phone'])) {
                 $user->phone = $validated['phone'];
             }
             if (isset($validated['avatar'])) {
                 $user->avatar = $validated['avatar'];
             }
             if (isset($validated['password'])) {
                 $user->password = Hash::make($validated['password']);
             }

             $user->save();

             return response()->json([
                 'user' => $user,
                 'message' => 'Profile updated successfully'
             ]);
         }
     }