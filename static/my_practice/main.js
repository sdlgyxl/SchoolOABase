Vue.component('balance', {
    template: `
    <div>
        <show @show-balance="show_balance=true"></show>
        <div v-if="show">
            您的余额：
        </div>
    </div>
    `,
    methods: {
        show_balance: function (s,data) {
            alert(1);
            this.show = true;
            console.log(data);
        }
    },
    data: function () {
        return {
            show: false,
        }
    },

});
Vue.component('show', {
    template: '<button @click="on_click()">显示余额</button>',
    methods: {
        on_click: function () {
            this.$emit('show-balance', {a: 1, b: 2});
        }
    }
});

new Vue({
    el: "#app",
});