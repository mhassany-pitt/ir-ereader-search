import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  courses: any = [];
  filter = '';

  constructor(
    private http: HttpClient
  ) { }

  ngOnInit(): void {
    this.load();
  }

  get courses_filtered() {
    return this.filter
      ? this.courses.filter((c: any) => c.title.toLowerCase().indexOf(this.filter.toLowerCase()) > -1)
      : this.courses;
  }

  load() {
    this.http.get(`${environment.apiUrl}/courses`).subscribe({
      next: (value: any) => this.courses = value,
      error(err) {
        alert('oops!!! i could not load the data; my bad.');

        console.log(err);
      }
    });
  }
}
