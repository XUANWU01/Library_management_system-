$(document).ready(function () {
    $('#loginSubmit').on('click', function (e) {
        e.preventDefault();

        // 表单验证逻辑
        const studentNumber = $('#studentNumber').val().trim();
        const name = $('#name').val().trim();
        const password = $('#password').val().trim();

        if (!studentNumber || !name || !password) {
            alert('所有字段均为必填项，请填写完整。');
            return;
        }

        // 检查密码强度，这里假设checkPasswordStrength返回true/false
        if (!checkPasswordStrength()) {
            alert('密码强度不足，请设置更复杂的密码。');
            return;
        }

        // 数据清理和格式化，如果有需要的话
        // ...

        // 准备数据发送到后端
        const postData = {
            studentNumber: studentNumber,
            name: name,
            password: password // 注意：实际应用中密码通常需要加密处理再发送
        };

        // 发送请求到正确的后端URL，这里仅为示例
        const url = 'YOUR_BACKEND_LOGIN_API_ENDPOINT'; // 替换为实际的API地址
        sendAjaxRequest(url, postData, function (response) {
            // 成功的处理逻辑
            if (response.success) {
                alert('登录成功！');
                // 跳转到主页或其他逻辑
            } else {
                alert(response.message || '登录失败，请重试。');
            }
        }, function (jqXHR, textStatus, errorThrown) {
            // 失败的处理逻辑
            alert('请求失败，请检查网络连接。');
        });
    });
    // ... 其他脚本内容 ...
});