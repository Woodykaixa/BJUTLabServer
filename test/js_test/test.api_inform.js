

describe('测试Inform API', () => {
    describe('通知发布', () => {

        it('发布临时通知', (done) => {

            const loginForm = new FormData();
            loginForm.append('id', 'G18074104');
            loginForm.append('password', 'ASDads64770');
            loginForm.append('type', 2);
            postTo('/Auth/login', loginForm);
            const date = new Date()
            const form = new FormData();
            form.append('title', 'API [POST]/Inform/inform测试');
            form.append('content', '使用浏览器测试发布通知的API');
            form.append('type', 0);
            form.append('create', date.format());
            date.setDate(date.getDate() + 1);
            form.append('expire', date.format());
            fetch(api('/Inform/inform'), {
                method: 'POST',
                credentials: 'include',
                body: form
            }).then(res => {
                done();
                return res.json();
                expect(res.status).to.eql(200);
            }).then(json => {
                expect(json['err']).to.eql(undefined);
                console.log(json)
                expect(json['return code']).to.eql(0);
            }).catch(err => {
                done(err);
            });
        });
        it('发布长期通知', (done) => {
            const date = new Date()
            const form = new FormData();
            form.append('title', 'API [POST]/Inform/inform测试');
            form.append('content', '使用浏览器测试发布通知的API');
            form.append('type', 1);
            form.append('create', date.format());
            fetch(api('/Inform/inform'), {
                method: 'POST',
                credentials: 'include',
                body: form
            }).then(res => {
                done();
                expect(res.status).to.eql(200);
                return res.json();
            }).then(json => {
                expect(json['err']).to.eql(undefined);
                console.log(json)
                expect(json['return code']).to.eql(0);
            }).catch(err => {
                done(err);
            });
        });
    });



});
