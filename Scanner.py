from BadTokenExpection import BadTokenExpection


class Scanner:
    @staticmethod
    def scan(content: str):
        """
        Will take a string and tell you what the tokens are
        and what the token values are
        """
        tokens = []
        tokenValues = []
        position = 0

        while position < len(content):
            # cc is short for current character
            cc = content[position]

            # If the current letter is a string
            if cc == '(':
                tokens.append('lparen')
                tokenValues.append(cc)
            elif cc == ')':
                tokens.append('rparen')
                tokenValues.append(cc)
            elif cc == '+':
                tokens.append('plus')
                tokenValues.append(cc)
            elif cc == '-':
                tokens.append('minus')
                tokenValues.append(cc)
            elif cc.isalpha():
                finalWord = cc
                # While the next character is a letter
                while not Scanner.isAtEndOfString(position, content) and content[position + 1].isalnum():
                    finalWord += content[position + 1]
                    position += 1

                # If the final word is either read or write
                if any(readOrWrite in finalWord for readOrWrite in ['read', 'write']):
                    tokens.append(finalWord)
                else:
                    tokens.append('id')

                tokenValues.append(finalWord)
            # If the current character is a digit
            elif cc.isdigit():
                number = ""

                # Look for all digits and maybe 1 decimal point
                seenDecimalPoint = False
                doneReading = False

                while not doneReading:
                    number += content[position]
                    if Scanner.isAtEndOfString(position, content):
                        doneReading = True
                    elif content[position + 1].isdigit():
                        position += 1
                    elif content[position + 1] == '.':
                        if seenDecimalPoint:
                            raise BadTokenExpection()
                        else:
                            position += 1
                            seenDecimalPoint = True
                    elif content[position + 1].isspace():
                        doneReading = True
                        position += 1
                    else:
                        raise BadTokenExpection()

                tokens.append('number')
                tokenValues.append(number)
            # If we see a decimal point
            elif cc == '.':
                number = ""
                doneReading = False
                while not doneReading:
                    number += content[position]
                    if content[position + 1].isdigit():
                        position += 1
                    elif content[position + 1].isspace():
                        doneReading = True
                    else:
                        raise BadTokenExpection()

                tokens.append('number')
                tokenValues.append(number)
            # Check for proper assignment
            elif cc == ':':
                if Scanner.nextCharacterMatches(position, content, '='):
                    tokens.append('assign')
                    tokenValues.append(':=')
                    position += 1
                else:
                    raise BadTokenExpection()
            # Check for division and for comments
            elif cc == '/':
                readingComment = True

                while (readingComment):
                    # Single line comments
                    if Scanner.nextCharacterMatches(position, content, '/'):
                        while not Scanner.nextCharacterMatches(position, content, '\n'):
                            position += 1
                        readingComment = False
                    # Multi-line Comments
                    elif Scanner.nextCharacterMatches(position, content, '*'):
                        # Look for the */
                        while True:
                            if Scanner.nextCharacterMatches(position, content, '*') and Scanner.nextCharacterMatches(position + 1, content, '/'):
                                position += 2
                                readingComment = False
                                break
                            position += 1
                    else:
                        readingComment = False
                        tokens.append('div')
                        tokenValues.append('/')
            # Skip all spaces
            elif cc.isspace():
                pass
            # Anything else not recognized by scanner
            else:
                raise BadTokenExpection()

            position += 1
        return tokens, tokenValues

    @staticmethod
    def nextCharacterMatches(currentPostion: int, content: str, match):
        if currentPostion + 1 == len(content):
            return False
        else:
            return content[currentPostion + 1] == match

    @staticmethod
    def prevCharacterMatches(currentPostion: int, content: str, match):
        if currentPostion == 0:
            return False
        else:
            return content[currentPostion - 1] == match

    @staticmethod
    def isAtEndOfString(currentPostion: int, content: str):
        return currentPostion + 1 == len(content)
