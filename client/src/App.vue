<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>
<script>

export default {
  name: 'App',
  methods: {
     sendAddress(address) {
      var constraint = {}
      var formData = new URLSearchParams();
      constraint['address'] = address;
      constraint = JSON.stringify(constraint)
      formData.append('constraint', constraint)
      this.sendUrl('searchAddress', formData, 'address', address)
    },
    sendUrl(Url, formData, v_id, info) {
      var self=this
      Url = 'http://127.0.0.1:22068/' + Url
      console.log('Request: ', Url)
      self.$api.post(Url, formData, data => {
        console.log('get ' + v_id + 'success: ', data)

      })
    }
  },
  mounted() {
    let self = this
    var address = '1DUMifqLdCRvx6tAzafwDC2tKRntRAAm3z'
    this.sendAddress(address)
  }
}

</script>
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

</style>
