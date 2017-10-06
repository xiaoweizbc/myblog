'use strict';
$(function() {
	// 初始化七牛SDK代码
	// 初始化七牛的代码必须放在选择图片行为之前
	var domain = 'http://owspqn974.bkt.clouddn.com/'; // xiaoweizbc：test（华东）
    var uploader = Qiniu.uploader({
		runtimes: 'html5,flash,html4', // 上传模式，依次退化
		browse_button: 'pickfiles', // 上传选择的点选按钮，必须
		container: 'container',	// 上传区域DOM的ID，默认是browse_button的父元素
		drop_element: 'container', // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
		max_file_size: '500mb', // 文件最大允许的尺寸
		dragdrop: true, // 是否开启拖拽上传
		chunk_size: '4mb', // 分块上传时，每片的大小
		uptoken_url: '/cms/get_token/', // ajax请求token的url
		domain: domain, // 图片下载时候的域名
		get_new_uptoken: false, // 是否每次上传文件都要从业务服务器获取token
		auto_start: true, // 如果设置了true,只要选择了图片,就会自动上传
		log_level: 1, // log级别：5有debug信息，其他没有
		init:{
			'FilesAdded': function(up,files) {
				console.log('file added');
			},
			'BeforeUpload': function(up,file) {
				console.log('before upload');
			},
			'UploadProgress': function() {
				console.log('upload progress');
			},
			'FileUploaded': function(up,file,info) {
				console.log('file uploaded-----------');
				// 发送文件名到服务器
				var avatar = domain + file.name; // 设置图片的完成URL路径
				$('#pickfiles').attr('src',avatar) // 把图片的URL设置进img标签
				console.log('pickfiles path='+$('#pickfiles').attr('src'));
			},
			'Error': function(up,err,errTip) {
				console.log('error:'+err);
			}
		},
	});

	// 提交按钮执行事件
	$('.submit-btn').click(function(event) {
		console.log("点击了“保存”按钮")
		event.preventDefault();
		var username = $('.username-input').val();
		var avatar = null;
		console.log("username =", username)
		console.log("avatar =", avatar)
        console.log('pickfiles path='+$('#pickfiles').attr('src'));
		if(uploader.files.length > 0){ // 说明有图片上传了，则设置avatar的值，否则avatar = null
			avatar = $('#pickfiles').attr('src'); // src属性代表的就是上传的头像URL
		}
		var data = {'username':username};
		if(avatar){
			data['avatar'] = avatar;
		}
		console.log("data =", data)
		myajax.post({
			'url': '/cms/update_profile/',
			'data':data,
			'success': function(data) {
				if(data['code'] == 200){
					var alert = $('.alert-success');
					alert.html('更新成功');
					alert.show();
				}
			},
			'error': function(error) {
				console.log(error);
			},
		});
	});
});
