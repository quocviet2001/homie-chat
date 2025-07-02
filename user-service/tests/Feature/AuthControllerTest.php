<?php
     namespace Tests\Feature;

     use Illuminate\Foundation\Testing\RefreshDatabase;
     use Tests\TestCase;
     use App\Models\User;

     class AuthControllerTest extends TestCase
     {
         use RefreshDatabase;

         public function test_register_success()
         {
             // Gửi yêu cầu đăng ký
             $response = $this->postJson('/api/register', [
                 'name' => 'Test User',
                 'email' => 'test@example.com',
                 'password' => 'password123',
                 'phone' => '1234567890',
                 'avatar' => 'http://example.com/avatar.jpg'
             ]);

             $response->assertStatus(201)
                      ->assertJsonStructure(['user', 'token', 'message']);
             $this->assertDatabaseHas('users', ['email' => 'test@example.com']);
         }

         public function test_login_success()
         {
             User::create([
                 'name' => 'Test User',
                 'email' => 'test@example.com',
                 'password' => bcrypt('password123'),
             ]);

             // Gửi yêu cầu đăng nhập
             $response = $this->postJson('/api/login', [
                 'email' => 'test@example.com',
                 'password' => 'password123'
             ]);

             $response->assertStatus(200)
                      ->assertJsonStructure(['user', 'token', 'message']);
         }

         public function test_login_invalid_credentials()
         {
             // Gửi yêu cầu với thông tin sai
             $response = $this->postJson('/api/login', [
                 'email' => 'test@example.com',
                 'password' => 'wrongpassword'
             ]);

             $response->assertStatus(401)
                      ->assertJson(['error' => 'Invalid credentials']);
         }
     }