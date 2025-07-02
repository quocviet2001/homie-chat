<?php
     namespace App\Http\Controllers;

     use Illuminate\Http\Request;
     use App\Models\User;
     use Illuminate\Support\Facades\Hash;
     use Tymon\JWTAuth\Facades\JWTAuth;

     class AuthController extends Controller
     {
         public function register(Request $request)
         {
             $validated = $request->validate([
                 'name' => 'required|string|max:255',
                 'email' => 'required|string|email|max:255|unique:users',
                 'password' => 'required|string|min:6',
                 'phone' => 'nullable|string|max:20',
                 'avatar' => 'nullable|string|max:255',
             ]);

             $user = User::create([
                 'name' => $validated['name'],
                 'email' => $validated['email'],
                 'password' => Hash::make($validated['password']),
                 'phone' => $validated['phone'],
                 'avatar' => $validated['avatar'],
             ]);

             $token = JWTAuth::fromUser($user);

             return response()->json([
                 'user' => $user,
                 'token' => $token,
                 'message' => 'Registration successful'
             ], 201);
         }

         public function login(Request $request)
         {
             $credentials = $request->validate([
                 'email' => 'required|string|email',
                 'password' => 'required|string',
             ]);

             if (!$token = JWTAuth::attempt($credentials)) {
                 return response()->json(['error' => 'Invalid credentials'], 401);
             }

             $user = JWTAuth::user();

             return response()->json([
                 'user' => $user,
                 'token' => $token,
                 'message' => 'Login successful'
             ]);
         }

         public function logout()
         {
             JWTAuth::invalidate(JWTAuth::getToken());
             return response()->json(['message' => 'Logout successful']);
         }
     }