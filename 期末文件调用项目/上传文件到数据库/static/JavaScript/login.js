/**
 * 检测密码强度并显示相应提示
 */
function checkPasswordStrength() {
    const password = document.getElementById('password'); // 获取密码输入框元素
    const strengthMessage = document.getElementById('passwordStrength'); // 获取密码强度提示元素
    // const strengthMessage = document.getElementById('passwordStrength2'); // 获取密码强度提示元素
    let strength = 0; // 初始化密码强度计数器

    // 遍历简单的密码强度规则
    if (password.value.length >= 8) strength++; // 至少8个字符
    if (/[a-z]/.test(password.value)) strength++; // 至少一个小写字母
    if (/[A-Z]/.test(password.value)) strength++; // 至少一个大写字母
    if (/\d/.test(password.value)) strength++; // 至少一个数字
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password.value)) strength++; // 至少一个特殊字符

    // 根据强度等级显示提示
    switch (strength) {
        case 0:
        case 1:
            strengthMessage.textContent = '弱口令'; // 显示“弱口令”提示
            strengthMessage.className = 'password-strength weak'; // 设置CSS类
            break;
        case 2:
        case 3:
            strengthMessage.textContent = '一般'; // 显示“一般”提示
            strengthMessage.className = 'password-strength medium'; // 设置CSS类
            break;
        default:
            strengthMessage.textContent = '强密码'; // 显示“强密码”提示
            strengthMessage.className = 'password-strength strong'; // 设置CSS类
            break;
    }

    // 根据密码是否符合最低要求控制提示的可见性
    if (strength === 0) {
        strengthMessage.style.display = 'none'; // 隐藏提示
    } else {
        strengthMessage.style.display = 'inline'; // 显示提示
    }
}

// /**
 // * 发送AJAX请求，封装以提高代码复用性和可维护性
 // * @param {string} url - 请求的URL
 // * @param {Object} data - 要发送的数据
 // * @param {function} successCallback - 请求成功时调用的回调函数
 // * @param {function} errorCallback - 请求失败时调用的回调函数
 // */
//
//
// function sendAjaxRequest(url, data, successCallback, errorCallback) {
//     $.ajax({
//         url: '', // 请求的URL
//         type: 'POST', // 请求类型
//         dataType: 'json', // 预期的响应数据类型
//         contentType: 'application/x-www-form-urlencoded', // 数据内容类型
//         data: data, // 要发送的数据
//         success: function (response) {
//             console.log('请求成功:', response); // 打印请求成功的响应
//             if (typeof successCallback === 'function') {
//                 successCallback(response); // 调用成功回调
//             }
//             if (response.status === 'success') {
//                 // 登录成功，跳转到首页
//                 window.location.href = '/';
//             }
//             if (response.status === 'error') {
//                 // 登录失败，显示错误信息
//                 alert(response.message);
//             }
//         }
//         ,
//         error: function (jqXHR, textStatus, errorThrown) {
//             console.error('请求失败:', textStatus, errorThrown); // 打印请求失败的信息
//             if (typeof errorCallback === 'function') {
//                 errorCallback(jqXHR, textStatus, errorThrown); // 调用失败回调
//             } else {
//                 alert('请求失败，请稍后再试。'); // 默认失败回调
//             }
//         }
//     });
// }

//
// $(document).ready(function () {
//     // 阻止表单提交的默认行为，使用AJAX发送登录请求
//     $('#loginSubmit').on('click', function (e) {
//         e.preventDefault();
//
//         // 示例：发送包含两个键值对的POST请求
//         const url = '/login';
//         const data = {
//             account: $('#account').val(),
//             password: $('#password').val()
//         };
//
//         sendAjaxRequest(url, data, function (response) {
//             // 请求成功时的处理逻辑
//             if (response.success) {
//                 // 登录成功，跳转到首页或其他页面
//                 window.location.href = '/index';
//             } else {
//                 // 登录失败，显示错误信息
//                 alert(response.message);
//             }
//         }, function (jqXHR, textStatus, errorThrown) {
//             // 请求失败时的处理逻辑
//             alert('请求失败，请检查网络连接。' + (errorThrown ? ' 错误信息：' + errorThrown : ''));
//         });
//     });
// });
