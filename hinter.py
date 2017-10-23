import re


class hinter():
    def hint(self, infile):
        to_check_format = []
        to_merge_timeframes = []
        to_return = {}
        with open(infile, "r") as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
        maxItem = len(lines)
        if maxItem < 2:
            return to_return
        for first_counter in range(0, maxItem):
            fresult = self.extract(lines[first_counter])
            if fresult is None:
                to_check_format.append((first_counter, lines[first_counter]))
                print "Check format of " + str(to_check_format[-1])
                continue
            for second_counter in range(first_counter + 1, maxItem):
                second_result = self.extract(lines[second_counter])
                if second_result is None:
                    to_check_format.append((second_counter, lines[second_counter]))
                    continue
                # print first_counter
                # print second_counter
                halves = 2
                similar = self.check_similarity(lines[first_counter], lines[second_counter])
                if similar:
                    pass
                    # print "Consider Merging the time frames"
                self.check_precedence(lines[first_counter], lines[second_counter])

    def check_precedence(self, first_entry, second_entry):
        to_merge_time_frame = []
        to_create_new = []
        to_swap = []
        first_halves = self.extract(first_entry)
        second_halves = self.extract(second_entry)
        first_details = first_halves["Details"]
        second_details = second_halves["Details"]
        first_cols = first_details.split("|")[:-1]
        second_cols = second_details.split("|")[:-1]
        if len(first_cols) != len(second_cols):
            raise ValueError("Unmatching number of columns between " + first_entry + " and " + second_entry)
        number_of_columns = len(first_cols)
        # keys ( 1:Exact , 2:Substring , 3:Different , 0:Unknown)
        state = [0] * number_of_columns
        first_alert = [False] * number_of_columns
        second_alert = [False] * number_of_columns
        for i in range(0, number_of_columns):
            # print "Item i: "+str(i)
            first_item = first_cols[i]
            second_item = second_cols[i]
            first_raw = first_item.replace("*", "")
            second_raw = second_item.replace("*", "")
            # print "First Item: "+first_item
            # print "Second Item: "+second_item
            if first_item != "*":
                first_pattern = first_item.replace("*", ".*")
            else:
                first_pattern = ".*"

            if second_item != "*":
                second_pattern = second_item.replace("*", ".*")
            else:
                second_pattern = ".*"

            first_match_result = re.search(first_pattern, second_raw)
            second_match_result = re.search(second_pattern, first_raw)

            first_alert[i] = (second_match_result is not None)
            second_alert[i] = (first_match_result is not None)

        # print first_cols
        # print second_cols
        # print first_alert
        # print second_alert
        state = [(first_alert[i], second_alert[i]) for i in range(0, number_of_columns)]
        # print state
        if (False, False) in state:
            # print "Do nothing, completely different"
            pass
        elif (False, True) in state and (True, False) in state:
            if (len(first_halves["TimeFrame"])):
                if (len(second_halves["TimeFrame"])):
                    print "Consider creating a new entry for:"
                    to_create_new.append((first_entry,second_entry))

                else:
                    print "Consider swapping the entries:"
                    to_swap.append((first_entry,second_entry))

                print "\t" + first_entry
                print "\t" + second_entry
        elif (False, True) in state:
            column = state.index((False,True))
            if (len(first_halves["TimeFrame"])):
                if len(second_halves["TimeFrame"]):
                    print "Consider creating a new entry for:"
                    to_create_new.append((first_entry,second_entry))
                    print "\t" + first_entry
                    print "\t" + second_entry
                    to_create_new.append((first_entry,second_entry))
                    print "Suggestion: "+self.mergeEntries_generalization(first_entry,second_entry,column)
                else:
                    print "Consider swapping the entries:"
                    to_swap.append((first_entry,second_entry))
                    print "\t" + first_entry
                    print "\t" + second_entry
        elif (True, False) in state:
            if (len(first_halves["TimeFrame"])):
                print "Consider swapping the entries:"
                to_swap.append((first_entry,second_entry))
                print "\t" + first_entry
                print "\t" + second_entry
            # print "Some overlap"
            pass
        else:
            if len(first_halves["TimeFrame"]):
                if len(second_halves["TimeFrame"]):
                    print "Consider Merging the time frames and deleting old ones"
                    to_merge_time_frame.append((first_entry,second_entry))
                    print "\t" + first_entry
                    print "\t" + second_entry
                    print "Suggestion: "+self.mergeTimeFrames(first_entry,second_entry)
                else:
                    print "Consider Swapping the entries"
                    to_swap.append((first_entry,second_entry))
                    print "\t" + first_entry
                    print "\t" + second_entry

        # print

        to_return = {}
        to_return["Merge"] = to_merge_time_frame
        to_return["Create"] = to_create_new
        to_return["Swap"] = to_swap

        return to_return

    def extract(self, entry):
        to_return = {}
        columns = 6
        pattern = "(?P<Details>^(.*\|){" + str(columns) + "})(?P<TimeFrame>(\[.+\]\s*$)?)"
        result = re.search(pattern, entry)
        if result is not None:
            to_return["Details"] = result.group("Details")
            to_return["TimeFrame"] = [x.strip().replace("[", "").replace("]", "") for x in
                                      result.group("TimeFrame").split(",") if len(x.strip())]
        else:
            return None
        return to_return

    def check_similarity(self, first_entry, second_entry):
        #print first_entry + " <<<<<< ------- >>>>>> " + second_entry

        first = self.extract(first_entry)
        second = self.extract(second_entry)
        if first is None:
            raise ValueError("Check format of the entry: " + first_entry)
        elif second is None:
            raise ValueError("Check format of the entry: " + second_entry)
        to_return = (first["Details"] == second["Details"])
        return to_return

    def lookup(self,Details,TimeFrames):
        to_return = []
        for line in lines:
            halves = self.extract(line)
            if halves["Details"] == Details and subset(halves["TimeFrame"],TimeFrames):
                to_return.append(line)

        return to_return

    def subset(self,bigger_list,smaller_list):
        is_subset = all((x in smaller_list) for x in bigger_list)
        return is_subset

    def createEntry(self,Details,TimeFrame):
        entry = Details+"["+",".join(TimeFrame)+"]"
        return entry

    def mergeTimeFrames(self,first_entry,second_entry):
        first_halves = self.extract(first_entry)
        second_halves = self.extract(second_entry)
        if first_halves["Details"] != second_halves["Details"]:
            raise ValueError("mergeTimeFrame: mismatching details for:\n\t"+first_entry+"\n\tand\n\t"+second_entry)
        new_time_frame = list(set(first_halves["TimeFrame"]+second_halves["TimeFrame"]))
        new_entry = self.createEntry(first_halves["Details"],new_time_frame)
        return new_entry

    def mergeEntries_generalization(self,first_entry,second_entry,column):
        first_halves = self.extract(first_entry)
        second_halves = self.extract(second_entry)
        first_raw = first_halves["Details"].split("|")[column].replace("*","")
        second_raw = second_halves["Details"].split("|")[column].replace("*","")
        new_details = ""
        if len(first_raw) == len(second_raw):
            raise ValueError("mergeEntries_generalization: Misuse")
        elif len(first_raw) > len(second_raw):
            new_details = first_halves["Details"]

        else:
            new_details = second_halves["Details"]
        new_time_frame = list(set(first_halves["TimeFrame"]+second_halves["TimeFrame"]))
        new_entry = self.createEntry(new_details,new_time_frame)
        return new_entry


