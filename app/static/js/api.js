/**
 * api.js - Module xử lý API calls cho ứng dụng chat RESTful
 * File này chứa tất cả các hàm giao tiếp với server RESTful API
 */

// Lấy session conversation ID hiện tại từ UI
function getCurrentConversationId() {
    return document.getElementById('user-id')?.textContent || '';
}

// Hàm gửi tin nhắn chat sử dụng RESTful API
async function sendChatMessage(message) {
    const conversationId = getCurrentConversationId();
    const url = `/api/conversations/${conversationId}/messages?use_session=true&create_if_missing=true&format=html`;
    
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { response: data.data.ai_response };
}

// Hàm tạo cuộc hội thoại mới sử dụng RESTful API
async function createNewConversationAPI() {
    const response = await fetch('/api/conversations?use_session=true', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return { 
        success: true, 
        chat_id: data.data.id,
        message: data.message 
    };
}

// Hàm tải cuộc hội thoại sử dụng RESTful API
async function loadConversationAPI(chatId) {
    const response = await fetch(`/api/conversations/${chatId}/active`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    // Get conversation data
    const historyResponse = await fetch(`/api/conversations/${chatId}?format=json`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!historyResponse.ok) {
        const errorData = await historyResponse.json();
        throw new Error(errorData.error || `HTTP error! status: ${historyResponse.status}`);
    }
    
    const historyData = await historyResponse.json();
    return { 
        success: true, 
        chat_history: historyData.data
    };
}

// Hàm xóa cuộc hội thoại sử dụng RESTful API
async function deleteConversationAPI(chatId) {
    const response = await fetch(`/api/conversations/${chatId}?create_new=true`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (response.status === 204) {
        return { success: true, message: 'Đã xóa hội thoại thành công!' };
    }
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return { success: true, message: 'Đã xóa hội thoại thành công!' };
}

// Hàm lấy danh sách các cuộc hội thoại sử dụng RESTful API
async function getConversationsAPI() {
    const response = await fetch('/api/conversations', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return { conversations: data.data };
}

// Export tất cả các hàm API
export {
    sendChatMessage,
    createNewConversationAPI,
    loadConversationAPI,
    deleteConversationAPI,
    getConversationsAPI
};
