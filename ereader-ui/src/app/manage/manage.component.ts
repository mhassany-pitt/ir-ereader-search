import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.less']
})
export class ManageComponent implements OnInit {

  pendingIndex = false;
  courses: any = [];

  constructor(
    private http: HttpClient
  ) { }

  ngOnInit(): void {
    this.load();
  }

  load() {
    this.http.get(`${environment.apiUrl}/index`, {}).subscribe({
      next: (value: any) => this.pendingIndex = true,
      error: (err) => this.pendingIndex = false,
    });

    this.http.get(`${environment.apiUrl}/courses`).subscribe({
      next: (value: any) => this.courses = value,
      error(err) {
        alert('oops!!! i could not load the data; my bad.');

        console.log(err);
      }
    });
  }

  indexUpdates() {
    this.http.patch(`${environment.apiUrl}/index`, {}).subscribe({
      next: (value: any) => alert('ok! done.'),
      error(err) {
        alert('oops!!! i could not index updates; my bad.');

        console.log(err);
      }
    });
  }
}
