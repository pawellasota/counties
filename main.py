import territory
import ui


def main():
    territory.Territory.import_csv("malopolska.csv")
    new_territory = territory.Territory()
    new_territory.create_objects()
    while True:
        ui.handle_menu("main")
        options = ui.get_inputs([""], "Your choice")
        if options[0] == "1":
            ui.print_table([new_territory.count_entities()], ["Województwo", "Powiaty", "Gminy miejskie", "Gminy wiejskie",
                           "Gminy miejsko-wiejskie", "Obszary wiejskie", "Miasta",
                           "Miasta na prawach powiatu", "Delegatury"], 
                           "Statistics", False)
        elif options[0] == "2":
            ui.print_table([new_territory.cities_with_longest_names()], ["First city", "Second city", "Third city"], 
                           "3 cities with longest names")
        elif options[0] == "3":
            ui.print_table([[new_territory.counties_with_largest_communities()]], 
                           ["County's name"], "County with the largest number of communities")
        elif options[0] == "4":
            ui.print_table(new_territory.locations_with_several_categories(), 
                           ["Locations name", "Number of categories"], "Locations, that belong to more than one category")
        elif options[0] == "5":
            options = ui.get_inputs(["Type search string: "], "Advanced search")
            output = new_territory.advanced_search(options[0])
            if not output:
                ui.print_error_message("No matches found.")
                continue
            ui.print_table(output, ["Name", "Type"], "Matches found:")
        elif options[0] == "0":
            break
        else:
            ui.print_error_message("No such option available.")


if __name__ == "__main__":
    main()