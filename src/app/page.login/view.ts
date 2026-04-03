import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
  constructor(public service: Service) {}

  public returnTo: string = "notset";
  @Input() title: any;
  public showSignup: boolean = false;
  public showPassword: boolean = false;
  public showResetPassword: boolean = false;
  public signupStep: number = 1;
  public resetStep: number = 1;
  public loaded = false;

  public user = {
    email: '',
    password: '',
    remember: false
  };

  public signupData = {
    name: '',
    email: '',
    password: '',
    password_repeat: ''
  };

  public resetData = {
    email: '',
    name: '',
    new_password: '',
    new_password_repeat: ''
  };

  public async ngOnInit() {
    await this.service.init();
    try {
      let returnTo = this.getParam('returnTo', '/main/user');
      let check = await this.service.auth.allow(false, returnTo);
      if (check) this.returnTo = returnTo;
    } catch (e) {
      this.returnTo = '/main/user';
    }
    this.loaded = true;
    await this.service.render();
  }

  public getParam(sname, defaultvalue) {
    let params = location.search.substring(location.search.indexOf("?") + 1);
    let sval = defaultvalue;
    params = params.split("&");
    for (let i = 0; i < params.length; i++) {
      let temp = params[i].split("=");
      if ([temp[0]] == sname) sval = temp[1];
    }
    return decodeURIComponent(sval);
  }

  public async alert(message: string, status: string = 'error', cancel: any = false, action: string = '확인') {
    return await this.service.alert.show({
      title: "",
      message: message,
      cancel: cancel,
      actionBtn: status,
      action: action,
      status: status
    });
  }

  public async toggleForm() {
    this.showSignup = !this.showSignup;
    this.showResetPassword = false;
    this.signupStep = 1;
    this.signupData = { name: '', email: '', password: '', password_repeat: '' };
    await this.service.render();
  }

  public async nextSignupStep() {
    if (this.signupStep === 1) {
      if (!this.signupData.name) return await this.alert("이름을 입력해주세요");
      this.signupStep = 2;
      await this.service.render();
    }
  }

  public async prevSignupStep() {
    if (this.signupStep > 1) {
      this.signupStep--;
      await this.service.render();
    }
  }

  public async showResetForm() {
    this.showResetPassword = true;
    this.showSignup = false;
    this.resetStep = 1;
    this.resetData = { email: '', name: '', new_password: '', new_password_repeat: '' };
    await this.service.render();
  }

  public async nextResetStep() {
    if (this.resetStep === 1) {
      if (!this.resetData.name || !this.resetData.email) return await this.alert("이름과 이메일을 모두 입력해주세요");
      let { code, data } = await wiz.call('verify_reset', { email: this.resetData.email, name: this.resetData.name });
      if (code !== 200) return await this.alert(data?.message || "존재하지 않는 계정입니다.");
      this.resetStep = 2;
      await this.service.render();
    }
  }

  public async prevResetStep() {
    if (this.resetStep > 1) {
      this.resetStep--;
      await this.service.render();
    }
  }

  public async backToLogin() {
    this.showResetPassword = false;
    this.showSignup = false;
    await this.service.render();
  }

  public async resetPassword() {
    if (this.resetStep < 2) return;
    if (!this.resetData.email || !this.resetData.name) {
      return await this.alert("이메일과 이름을 모두 입력해주세요.");
    }

    let newPw = this.resetData.new_password;
    let newPwRe = this.resetData.new_password_repeat;
    if (newPw.length < 8) return await this.alert("8글자 이상의 비밀번호를 설정해주세요");
    if (newPw.search(/[a-z]/i) < 0) return await this.alert("비밀번호에 알파벳을 포함해주세요");
    if (newPw.search(/[0-9]/) < 0) return await this.alert("비밀번호에 숫자를 포함해주세요");
    if (newPw !== newPwRe) return await this.alert("비밀번호가 일치하지 않습니다");

    let payload = {
      email: this.resetData.email,
      name: this.resetData.name,
      new_password: this.service.auth.hash(newPw)
    };

    let { code, data } = await wiz.call("reset_password", payload);
    if (code == 200) {
      await this.alert("비밀번호가 변경되었습니다. 로그인해주세요.", "success");
      this.showResetPassword = false;
      await this.service.render();
    } else {
      await this.alert(data?.message || "비밀번호 변경에 실패했습니다.");
    }
  }

  public async login() {
    let user = JSON.parse(JSON.stringify(this.user));
    if (user.password) user.password = this.service.auth.hash(user.password);
    else delete user.password;

    let { code, data } = await wiz.call("login", user);
    if (code == 200) {
      let returnTo = this.getParam('returnTo', '/main/user');
      location.href = returnTo;
    } else {
      await this.alert(data?.message || '로그인에 실패했습니다.', 'error');
    }
  }

  public async signup() {
    if (this.signupStep < 2) return;

    if (!this.signupData.email) return await this.alert("이메일을 입력해주세요");
    if (this.signupData.name.length == 0) return await this.alert("이름을 입력해주세요");
    let password = this.signupData.password;
    let password_re = this.signupData.password_repeat;
    if (password.length < 8) return await this.alert("8글자 이상의 비밀번호를 설정해주세요");
    if (password.search(/[a-z]/i) < 0) return await this.alert("비밀번호에 알파벳을 포함해주세요");
    if (password.search(/[0-9]/) < 0) return await this.alert("비밀번호에 숫자를 포함해주세요");
    if (password != password_re) return await this.alert("비밀번호가 일치하지 않습니다");

    let user = JSON.parse(JSON.stringify(this.signupData));
    delete user.password_repeat;
    user.password = this.service.auth.hash(user.password);

    let { code, data } = await wiz.call("join", user);

    if (code == 200) {
      await this.alert("회원가입이 완료되었습니다! 로그인해주세요.", "success");
      this.showSignup = false;
      await this.service.render();
    } else {
      await this.alert(data?.message || '회원가입에 실패했습니다.');
    }
  }
}
