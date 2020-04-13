const api = (route) => 'http://localhost:5000' + route;

const getLoginForm = (school_id, password, type) => {
    const form = new FormData();
    form.append('school_id', school_id);
    form.append('password', password);
    form.append('type', type);
    return form;
};

const getChangePwdForm = (old, New) => {
    const form = new FormData();
    form.append('old', old);
    form.append('new', New);
    return form;
}

const postTo = async (route, form) => {
    return await fetch(api(route), {
        method: 'POST',
        body: form,
        credentials: 'include'
    });
};

describe('测试Auth API', () => {
    it('测试api()生成的url是否正确', () => {
        expect(api('/')).to.eql('http://localhost:5000/');
    });
    describe('#Login test', () => {
        it('学生登录', (done) => {
            postTo('/Auth/login', getLoginForm('18074104', 'ASDads64770', 0))
                .then(res => res.json())
                .then(json => {
                    done();
                    expect(json['success']).to.eql(true);
                    expect(json['name']).to.eql('初雨墨');
                }).catch(err => {
                    done(err);
                });
        });

        it('教师登录', (done) => {
            postTo('/Auth/login', getLoginForm('18074104', 'ASDads64770', 1))
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    done();
                }).catch(err => {
                    done(err);
                    expect(err['err']).to.eql('Unsupported user type: 1');
                });
        });
        for (let typeCode = 2; typeCode < 5; typeCode++) {
            it(`登录测试: type = ${typeCode}`, (done) => {
                postTo('/Auth/login',
                    getLoginForm('What ever you fill', 'What ever you fill', typeCode))
                    .then(res => res.json())
                    .then(json => {
                        console.log(json);
                        done();
                    }).catch(err => {
                        done(err);
                        expect(err['err']).to.eql('Unsupported user type: ' + typeCode);
                    })
            });
        }
        it('学生登录，学号错误', (done) => {
            postTo('/Auth/login', getLoginForm('180741016', 'ASDads64770', 0))
                .catch(err => {
                    done(err);
                }).then(res => res.json()).then(json => {
                    console.log(json);
                    done();
                    expect(res['success']).to.eql(false)
                });
        });
        it('学生登录，密码错误', (done) => {
            postTo('/Auth/login', getLoginForm('18074104', 'ASDads', 0))
                .catch(err => {
                    done(err);
                }).then(res => res.json()).then(json => {
                    console.log(json);
                    done();
                    expect(res['success']).to.eql(false)
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
                    expect(json['err']).to.eql('Missing parameter: school_id');
                }).catch(err => {
                    done(err);
                });
        });
        it('学生登录，缺少密码', (done) => {
            const form = new FormData();
            form.append('school_id', 'What ever you fill');
            form.append('type', 0);
            postTo('/Auth/login', form)
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    done();
                    expect(json['err']).to.eql('Missing parameter: password');
                }).catch(err => {
                    done(err);
                });
        });
        it('学生登录，缺少登录类型', (done) => {
            const form = new FormData();
            form.append('school_id', 'Fill anything you want');
            form.append('password', 'What ever you fill');
            postTo('/Auth/login', form)
                .then(res => res.json())
                .then(json => {
                    console.log(json);
                    done();
                    expect(json['err']).to.eql('Missing parameter: type');
                }).catch(err => {
                    done(err);
                });
        });
    });
});