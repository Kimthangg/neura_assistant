/**
 * api.js - Module xử lý API calls cho ứng dụng chat
 * File này chứa tất cả các hàm giao tiếp với server API
 */

// Hàm gửi tin nhắn chat
async function sendChatMessage(message) {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }    return await response.json();
}

// Hàm tạo cuộc hội thoại mới
async function createNewConversationAPI() {
    const response = await fetch('/new_conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Hàm tải cuộc hội thoại
async function loadConversationAPI(chatId) {
    const response = await fetch(`/load_conversation/${chatId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Hàm xóa cuộc hội thoại
async function deleteConversationAPI(chatId) {
    const response = await fetch(`/delete_conversation/${chatId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Hàm lấy danh sách các cuộc hội thoại
async function getConversationsAPI() {
    const response = await fetch('/get_conversations', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Export tất cả các hàm API
export {
    sendChatMessage,
    createNewConversationAPI,
    loadConversationAPI,
    deleteConversationAPI,
    getConversationsAPI
};
