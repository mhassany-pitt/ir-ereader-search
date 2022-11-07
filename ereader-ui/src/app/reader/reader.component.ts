import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from 'src/environments/environment';
import { v4 as uuidv4 } from 'uuid';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-reader',
  templateUrl: './reader.component.html',
  styleUrls: ['./reader.component.less']
})
export class ReaderComponent implements OnInit {

  toc = false;
  course: any = {};

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer,
  ) {
    if (this.id)
      this.load();
  }

  get id() {
    return this.route.snapshot.params['id'];
  }

  ngOnInit(): void { }

  load() {
    this.http.get(`${environment.apiUrl}/courses/${this.id}`)
      .subscribe({
        next: (value: any) => {
          value.sections?.forEach((s: any) => {
            s.files?.forEach((f: any) => {
              const page_nums = []; // asc-sorted from 0
              for (let i = 0, l = f.page_count || 1; i < l; i++)
                page_nums.push(i);

              f.pages = [];
              let last_page_size: any = null;
              page_nums.forEach((p: any) => {
                if (f.page_size && p in f.page_size)
                  last_page_size = f.page_size[p];

                f.pages.push({
                  el_id: "ereader-p" + uuidv4(),
                  page_size: last_page_size?.split(',').map((e: string) => parseFloat(e) + 10 + 'pt'),
                  src_url: this.sanitizer.bypassSecurityTrustResourceUrl(
                    `${environment.apiUrl}/courses/${value.id}/${s.id}/${f.id}/${p}#toolbar=0&navpanes=0&scrollbar=0`
                  )
                })
              });
            });
          });

          this.course = value;
        },
        error(err) {
          alert('oops!!! i could not load the data; my bad.');

          console.log(err);
        }
      });
  }

  scrollTo(page: { el_id: string }) {
    document.querySelector('#' + page.el_id)?.scrollIntoView({ behavior: 'smooth' });
    this.toc = false;
  }
}
