//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    weather: {
      wendu: 18,
      ganmao: '昼夜温差较大，较易发生感冒',
      yesterday: {
        date: '17日星期四',
        type: '阴',
        fx: '南风',
        fl: '微风',
        low: '低温 8C',
        high: '高温 16C'
      },
      forecast: [
        {
          date: '18日星期五',
          type: '阴',
          high: '高温 16C',
          low: '低温 8C',
          fengxiang: '南风',
          fengli: '微风'
        }, {
          date: '18日星期五',
          type: '阴',
          high: '高温 16C',
          low: '低温 8C',
          fengxiang: '南风',
          fengli: '微风'
        }, {
          date: '18日星期五',
          type: '阴',
          high: '高温 16C',
          low: '低温 8C',
          fengxiang: '南风',
          fengli: '微风'
        }, {
          date: '18日星期五',
          type: '阴',
          high: '高温 16C',
          low: '低温 8C',
          fengxiang: '南风',
          fengli: '微风'
        }, {
          date: '18日星期五',
          type: '阴',
          high: '高温 16C',
          low: '低温 8C',
          fengxiang: '南风',
          fengli: '微风'
        }
      ]
    },
    today: '2016-11-18',
    city: '北京',
    inputCity: '',
  },

  onLoad: function (options) {
    this.setData({
      today: util.formatTime(new Date()).split(' ')[0] //当前日期
    });
    var self = this;
    wx.getLocation({
      type: 'wgs84', // 默认为 wgs84 返回 gps 坐标，gcj02 返回可用于 wx.openLocation 的坐标
      success: function (res) {
        wx.request({
          url: 'http://api.map.baidu.com/geocoder/v2/' + '?ak=ASAT5N3tnHIa4APW0SNPeXN5&location=' + res.latitude + ',' + res.longitute + '&output=json&pois=0',
          data: {},
          // method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
          header: { 'Content-Type': 'application/json' }, // 设置请求的 header
          success: function (res) {
            // success
            var city = res.data.result.addressComponent.city.replace('市', '');
            self.searchWeather(city);
          }
        })
      },
      fail: function () {
        // fail
      },
      complete: function () {
        // complete
      }
    })
  },

  searchWeather: function (cityName) {
    var self = this;
    wx.request({
      url: 'http://wthrcdn.etouch.cn/weather_mini?city=' + cityName,
      data: {},
      header: {
        'Content-Type': 'application/json'
      },
      success: function (res) {
        if (res.data.status == 1002) //无此城市
        {
          //显示错误信息
          wx.showModal({
            title: '提示',
            content: '输入的城市名称有误，请重新输入！',
            showCancel: false,
            success: function (res) {
              self.setData({ inputCity: '' });
            }
          })
        } else {
          var weather = res.data.data;  //获取天气数据

          for (var i = 0; i < weather.forecast.length; i++) {
            var d = weather.forecast[i].date;
            //处理日期信息，添加空格
            weather.forecast[i].date = '　' + d.replace('星期', '　星期');
          }
          self.setData({
            city: cityName,      //更新显示城市名称
            weather: weather,    //更新天气信息
            inputCity: ''        //清空查询输入框
          })
        }
      }
    })
  },

  inputing: function (e) {
    this.setData({ inputCity: e.detail.value });
  },
  bindSearch: function () {
    this.searchWeather(this.data.inputCity);
  }


})

