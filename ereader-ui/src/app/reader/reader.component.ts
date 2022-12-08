import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from 'src/environments/environment';
import { v4 as uuidv4 } from 'uuid';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-reader',
  templateUrl: './reader.component.html',
  styleUrls: ['./reader.component.less'],
})
export class ReaderComponent implements OnInit {
  toc = false;
  course: any = {};

  _searchQuery: string = '';
  set searchQuery(s: any) {
    if (typeof s == 'string') {
      this._searchQuery = s;
      console.log(typeof s);
    }
  }
  get searchQuery() {
    return this._searchQuery;
  }
  delayedSearch: any = null;
  searchResults: any[] = [];
  searchElIds: any = {};
  highlight: any = {};

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    public sanitizer: DomSanitizer
  ) {
    if (this.id) this.load();
  }

  get id() {
    return this.route.snapshot.params['id'];
  }

  ngOnInit(): void {}

  load() {
    // load the reading for the current course
    this.http.get(`${environment.apiUrl}/courses/${this.id}`).subscribe({
      next: (value: any) => {
        this.searchElIds = {};

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

              const el_id = 'ereader-p' + uuidv4();
              this.searchElIds[`s${s.id}f${f.id}p${p}`] = el_id;

              // prepare each html page
              f.pages.push({
                el_id,
                page_size: last_page_size
                  ?.split(',')
                  .map((e: string) => parseFloat(e) + 10 + 'pt'),
                src_url: `${environment.apiUrl}/courses/${value.id}/${s.id}/${f.id}/${p}`,
              });
            });
          });
        });

        this.course = value;
      },
      error(err) {
        alert('oops!!! i could not load the data; my bad.');

        console.log(err);
      },
    });
  }

  scrollTo(el_id: string) {
    // smoothly scorll to the specific page
    document.getElementById(el_id)?.scrollIntoView({ behavior: 'smooth' });
    this.toc = false;
  }

  search() {
    // with 500ms delay perform the search
    if (this.delayedSearch) clearInterval(this.delayedSearch);
    this.delayedSearch = setTimeout(
      () =>
        this.http
          .post(`${environment.apiUrl}/search`, {
            query: this.searchQuery,
            c_id: this.course.id,
          })
          .subscribe({
            next: (resp: any) => {
              // store the search result (will be rendered in the template)
              this.searchResults = resp.hits;
            },
            error(err) {
              alert('oops!!! i could not look that up; my bad.');

              console.log(err);
            },
          }),
      500
    );
  }

  searchSelected(result: any) {
    setTimeout(() => {
      // refresh the page and highlight the search result
      const doc = result.document;
      const sfp = `s${doc.s_id}f${doc.f_id}p${doc.fp_i}`;

      if (sfp in this.searchElIds) {
        const elId = this.searchElIds[sfp];
        this.highlight = {
          el_id: elId,
          param:
            '?highlight=' + encodeURIComponent(result.highlights[0].snippet),
        };
        this.scrollTo(elId);
      }

      this.searchQuery = '';
    }, 0);
  }
}
