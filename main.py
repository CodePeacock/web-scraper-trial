"""Run all scripts in order"""
import scraper
import excel_writer

scraper.iterate()
excel_writer.main()
