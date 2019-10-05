var Event = new Vue();

Vue.component('sayer', {
  template: `
    <div>
        我说:<input @keyup="on_change" v-model="i_said">
    </div> 
    `,
  data: function() {
    return {
      i_said: ''
    };
  },
  methods: {
    on_change: function() {
      Event.$emit('sayer-said-somthing', this.i_said);
    }
  }
});

Vue.component('shower', {
  template: `<div>发言人说:{{sayer_said}}</div>`,
  data: function() {
    return {
      sayer_said: ''
    };
  },
  mounted: function() {
    me = this;
    Event.$on('sayer-said-somthing', function(data) {
      console.log(data);
      me.sayer_said = data;
    });
  }
});

new Vue({
  el: '#app'
});
