<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\Friend;
use App\Models\FriendRequest;
use Tymon\JWTAuth\Facades\JWTAuth;

class FriendController extends Controller
{
    // Tìm kiếm bạn bè theo tên
    public function search(Request $request)
    {
        $request->validate([
            'query' => 'required|string|min:1'
        ]);

        $users = User::where('name', 'ilike', '%' . $request->query('query') . '%')
            ->where('id', '!=', JWTAuth::user()->id)
            ->get(['id', 'name', 'email', 'avatar']);

        return response()->json($users);
    }

    // Lấy danh sách bạn bè
    public function index()
    {
        $user = JWTAuth::user();
        $friends = $user->friends()->get(['users.id', 'users.name', 'users.email', 'users.avatar']);

        return response()->json($friends);
    }

    // Gửi lời mời kết bạn
    public function sendRequest(Request $request)
    {
        $request->validate([
            'receiver_id' => 'required|exists:users,id'
        ]);

        $user = JWTAuth::user();
        $receiver_id = $request->receiver_id;

        if ($user->id == $receiver_id) {
            return response()->json(['error' => 'Cannot send request to yourself'], 400);
        }

        $isFriend = $user->friends()->where('friend_id', $receiver_id)->exists();
        if ($isFriend) {
            return response()->json(['error' => 'Already friends'], 400);
        }

        $existingRequest = FriendRequest::where('sender_id', $user->id)
            ->where('receiver_id', $receiver_id)
            ->where('status', 'pending')
            ->exists();
        if ($existingRequest) {
            return response()->json(['error' => 'Request already sent'], 400);
        }

        FriendRequest::create([
            'sender_id' => $user->id,
            'receiver_id' => $receiver_id,
            'status' => 'pending'
        ]);

        return response()->json(['message' => 'Friend request sent']);
    }

    // Lấy danh sách lời mời kết bạn
    public function requests()
    {
        $user = JWTAuth::user();
        $requests = $user->receivedFriendRequests()
            ->where('status', 'pending')
            ->with(['sender' => function ($query) {
                $query->select('id', 'name', 'email', 'avatar');
            }])
            ->get();

        return response()->json($requests);
    }

    public function respondRequest(Request $request)
    {
        $request->validate([
            'request_id' => 'required|exists:friend_requests,id',
            'status' => 'required|in:accepted,rejected'
        ]);
        $user = JWTAuth::user();
        $friendRequest = FriendRequest::where('id', $request->request_id)
            ->where('receiver_id', $user->id)
            ->firstOrFail();

        $friendRequest->status = $request->status;
        $friendRequest->save();

        if ($request->status == 'accepted') {
            Friend::create([
                'user_id' => $friendRequest->sender_id,
                'friend_id' => $user->id,
            ]);
            Friend::create([
                'user_id' => $user->id,
                'friend_id' => $friendRequest->sender_id,
            ]);
        }

        $friendRequest->delete();
        return response()->json(['message' => "Friend request {$request->status}"]);
    }
}
