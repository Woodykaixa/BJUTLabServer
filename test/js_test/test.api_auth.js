
const getChangePwdForm = (old, New) => {
    const form = new FormData();
    form.append('old', old);
    form.append('new', New);
    return form;
};


describe('测试Auth API', () => {
    it('测试api()生成的url是否正确', () => {
        expect(api('/')).to.eql('http://localhost:5000/');
    });
    describe('登录测试', () => {
        it('学生登录', (done) => {
            postTo('/Auth/login', getLoginForm('18074104', 'ASDads64770', 0))
                .then(res => {
                    done();
                    expect(res.status).to.eql(200);
                    return res.json()
                })
                .then(json => {
                    expect(json['success']).to.eql(true);
                    expect(json['name']).to.eql('初雨墨');
                }).catch(err => {
                    done(err);
                });
        });

        it('教师登录', (done) => {
            postTo('/Auth/login', getLoginForm('18074104', 'ASDads64770', 1))
                .then(res => {
                    done();
                    expect(res.status).to.eql(400);
                    return res.json()
                })
                .then(json => {
                    console.log(json);
                    expect(json['err']).to.eql('Invalid parameter: unsupported user type: 1');
                }).catch(err => {
                    done(err);
                });
        });
        it('实验室管理员登录', (done) => {
            postTo('/Auth/login', getLoginForm('G18074104', 'ASDads64770', 2))
                .then(res => {
                    done();
                    expect(res.status).to.eql(200)
                    return res.json()
                }).then(json => {
                    expect(json['success']).to.eql(true);
                    expect(json['name']).to.eql('开发者kaixa');
                    expect(json['office']).to.eql('11号楼A314');
                    expect(json['phone']).to.eql(null);
                    expect(json['email']).to.eql('690750353@qq.com');
                }).catch(err => {
                    done(err);
                });
        });
        for (let typeCode = 3; typeCode < 6; typeCode++) {
            it(`登录测试: type = ${typeCode}`, (done) => {
                postTo('/Auth/login',
                    getLoginForm('What ever you fill', 'What ever you fill', typeCode))
                    .then(res => {
                        done();
                        expect(res.status).to.eql(400);
                        return res.json()
                    })
                    .then(json => {
                        console.log(json);
                        expect(json['err']).to.eql('Invalid parameter: unsupported user type: ' + typeCode);
                    }).catch(err => {
                        done(err);
                    })
            });
        }
        it('学生登录，学号错误', (done) => {
            postTo('/Auth/login', getLoginForm('18074101', 'ASDads64770', 0))
                .then(res => res.json()).then(json => {
                    console.log(json);
                    done();
                    expect(json['success']).to.eql(false)
                });
        });
        it('学生登录，密码错误', (done) => {
            postTo('/Auth/login', getLoginForm('18074104', 'ASDads', 0))
                .then(res => res.json()).then(json => {
                    console.log(json);
                    done();
                    expect(json['success']).to.eql(false)
                });
        });
        it('学生登录，缺少学号', (done) => {
            const form = new FormData();
            form.append('password', 'What ever you fill');
            form.append('type', 0);
            postTo('/Auth/login', form)
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    done();
                    expect(json['err']).to.eql('Missing parameter: id');
                }).catch(err => {
                    done(err);
                    expect(1).to.eql(2);
                });
        });
        it('学生登录，缺少密码', (done) => {
            const form = new FormData();
            form.append('id', 'What ever you fill');
            form.append('type', 0);
            postTo('/Auth/login', form)
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    done();
                    expect(json['err']).to.eql('Missing parameter: password');
                }).catch(err => {
                    done(err);
                    expect(1).to.eql(2);
                });
        });
        it('学生登录，缺少登录类型', (done) => {
            const form = new FormData();
            form.append('id', 'Fill anything you want');
            form.append('password', 'What ever you fill');
            postTo('/Auth/login', form)
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    done();
                    expect(json['err']).to.eql('Missing parameter: type');
                }).catch(err => {
                    done(err);
                    expect(1).to.eql(2);
                });
        });
    });
    describe('登出测试', () => {

        it('登出', (done) => {
            fetch(api('/Auth/logout'), { credentials: 'include' }).then(res => res.json())
                .then(json => {
                    done();
                    expect(json['msg']).to.eql('bye, 初雨墨');
                });
        });

    });
})
    ;