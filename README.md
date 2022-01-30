# Mapping of URN and Google Books ID of scans from Bavarian State Library

The [Bavarian State Library](https://www.bsb-muenchen.de/en/) has digitized huge amounts of books in [cooperation with Google Books](https://www.bsb-muenchen.de/ueber-uns/kooperationen/google/).
The scans are available via [Google Books](https://books.google.de/) in a handily usable way.
The quality of the scans available for download is scarse, however (only bw, low resolution).
Furthermore, it is unclear how permanent the Google Books IDs, by which scans can be referenced, actually are (cf. for example [this blog post](https://archivalia.hypotheses.org/64173)).

Neither the Google Book page nor the Google Books API (`https://www.googleapis.com/books/v1/volumes/<google_books_ID>`) indicates the source of the scans.

As I couldn't find any API that return the urn linked to the google books id, I iterated over the [dump of the Bavarian Union Catalog (B3kat)](https://www.bib-bvb.de/web/b3kat/open-data) (29.4M records) and retrieved the Google Books IDs (for books published before 1801) via the script the BSB catalogue uses to produce the link to Google Books. 

![](gb_link_bsb.png)

The Google Books ID is not part of the library metdata (consequently not to be found in the MARCXML).
The script requires the OCLC ID (contained in the MARCXML, field `035$a`) and returns the Google Books link.

Syntax of script:

`https://opacplus.bsb-muenchen.de/gbs/books?jscmd=viewapi&bibkeys=OCLC:<OCLC ID>`

The list `bvbgbs.csv` offers a list of the scans provided by the Bavarian State Library with OCLC ID, BVB ID, Google Books ID and (permanent) URN. Currently only scans of books published before 1801 are listed.

The list helps to transform google book links (of dubious permanence) into permanent links to scans in better resolution.
